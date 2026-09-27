#!/usr/bin/env python3
"""
Sincroniza o acervo vivo (Wiki.js) com o acervo pesquisável do assistente (Open WebUI)
e registra as lacunas (perguntas que o acervo não soube responder).

Syncs the living archive (Wiki.js) into the assistant's searchable archive (Open WebUI)
and records gaps (questions the archive could not answer).

Só usa a biblioteca padrão do Python. / Standard library only.

Como funciona:
  1. Lista as páginas publicadas da wiki.
  2. A camada vem do caminho da página:
        oficial/...   -> coleção "Documentos oficiais"
        memoria/...   -> coleção "Memória local"
        fichas/...    -> coleção "Fichas de solução"  (fichas/rascunhos/ é ignorado)
     Outras páginas (inicio, lacunas, curadoria/...) não vão para o assistente.
  3. Envia ao Open WebUI só as páginas novas ou alteradas; remove as apagadas.
  4. Fichas mais antigas que VALIDADE_FICHAS_MESES recebem um aviso no texto.
  5. Lê as lacunas gravadas pelo filtro (tools/filtro_lacunas.py) e atualiza a página
     "curadoria/lacunas" da wiki, visível só para curadores.

Variáveis de ambiente: WIKI_URL, WIKI_API_KEY, OWUI_URL, OWUI_API_KEY, ESTADO, LACUNAS,
VALIDADE_FICHAS_MESES, DOMINIO_ACERVO.

Uso manual / manual run:  python tools/sincronizar_acervo.py [--simular]
"""

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

CAMADAS = {
    "oficial/": ("Documentos oficiais", "Leis, planos, atos e cartilhas oficiais da cidade."),
    "memoria/": ("Memória local", "Entrevistas, histórias e estudos sobre a cidade, com consentimento."),
    "fichas/": ("Fichas de solução", "Como moradores resolveram problemas reais. Relatos revisados por curadores."),
}
IGNORAR = ("fichas/rascunhos/",)
PAGINA_LACUNAS = "curadoria/lacunas"

WIKI_URL = os.environ.get("WIKI_URL", "http://localhost:3000").rstrip("/")
WIKI_API_KEY = os.environ.get("WIKI_API_KEY", "")
OWUI_URL = os.environ.get("OWUI_URL", "http://localhost:8080").rstrip("/")
OWUI_API_KEY = os.environ.get("OWUI_API_KEY", "")
ESTADO = Path(os.environ.get("ESTADO", "sincronizacao.json"))
LACUNAS = Path(os.environ.get("LACUNAS", "lacunas.jsonl"))
VALIDADE_MESES = int(os.environ.get("VALIDADE_FICHAS_MESES", "12"))
DOMINIO_ACERVO = os.environ.get("DOMINIO_ACERVO", "")
SIMULAR = "--simular" in sys.argv


def log(msg: str) -> None:
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


# ---------- HTTP ----------

def http(method: str, url: str, token: str, dados=None, corpo: bytes | None = None,
         tipo: str = "application/json", timeout: int = 120):
    if dados is not None:
        corpo = json.dumps(dados).encode()
    req = urllib.request.Request(url, data=corpo, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if corpo is not None:
        req.add_header("Content-Type", tipo)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        texto = r.read().decode()
    return json.loads(texto) if texto else None


def graphql(consulta: str, variaveis: dict | None = None) -> dict:
    resp = http("POST", f"{WIKI_URL}/graphql", WIKI_API_KEY, {"query": consulta, "variables": variaveis or {}})
    if resp.get("errors"):
        raise RuntimeError(f"Wiki.js: {resp['errors']}")
    return resp["data"]


# ---------- Wiki.js ----------

def listar_paginas() -> list[dict]:
    dados = graphql("query { pages { list(orderBy: UPDATED, limit: 10000) "
                    "{ id path title updatedAt isPublished } } }")
    return dados["pages"]["list"]


def ler_pagina(pid: int) -> dict:
    dados = graphql("query($id: Int!) { pages { single(id: $id) "
                    "{ id path title description content updatedAt } } }", {"id": pid})
    return dados["pages"]["single"]


def camada_de(caminho: str):
    if any(caminho.startswith(p) for p in IGNORAR):
        return None
    for prefixo, info in CAMADAS.items():
        if caminho.startswith(prefixo):
            return info[0]
    return None


def meses_desde(iso: str) -> float:
    data = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - data).days / 30.44


def montar_documento(pagina: dict, camada: str) -> str:
    """Texto que o assistente vai indexar, com cabeçalho de procedência."""
    atualizado = pagina["updatedAt"][:10]
    link = f"https://{DOMINIO_ACERVO}/{pagina['path']}" if DOMINIO_ACERVO else pagina["path"]
    linhas = [
        f"# {pagina['title']}",
        "",
        f"Camada do acervo: {camada}",
        f"Endereço no acervo: {link}",
        f"Última atualização: {atualizado}",
    ]
    if camada == "Fichas de solução":
        linhas.append("Tipo de fonte: relato comunitário revisado (não é documento oficial)")
        if meses_desde(pagina["updatedAt"]) > VALIDADE_MESES:
            linhas.append(f"ATENÇÃO: esta ficha tem mais de {VALIDADE_MESES} meses e pode estar desatualizada.")
    if pagina.get("description"):
        linhas += ["", pagina["description"]]
    linhas += ["", pagina.get("content") or ""]
    return "\n".join(linhas)


def publicar_lacunas(texto: str) -> None:
    existentes = {p["path"]: p["id"] for p in listar_paginas()}
    comuns = {"content": texto, "description": "Perguntas que o acervo ainda não responde (gerado automaticamente)",
              "editor": "markdown", "isPrivate": False, "isPublished": True, "locale": "pt",
              "tags": ["lacunas"], "title": "Lacunas do acervo"}
    if PAGINA_LACUNAS in existentes:
        graphql("mutation($id: Int!, $content: String!, $description: String!, $editor: String!, "
                "$isPrivate: Boolean!, $isPublished: Boolean!, $locale: String!, $tags: [String]!, $title: String!) "
                "{ pages { update(id: $id, content: $content, description: $description, editor: $editor, "
                "isPrivate: $isPrivate, isPublished: $isPublished, locale: $locale, tags: $tags, title: $title) "
                "{ responseResult { succeeded message } } } }",
                {"id": existentes[PAGINA_LACUNAS], **comuns})
    else:
        graphql("mutation($content: String!, $description: String!, $editor: String!, $isPrivate: Boolean!, "
                "$isPublished: Boolean!, $locale: String!, $path: String!, $tags: [String]!, $title: String!) "
                "{ pages { create(content: $content, description: $description, editor: $editor, "
                "isPrivate: $isPrivate, isPublished: $isPublished, locale: $locale, path: $path, tags: $tags, "
                "title: $title) { responseResult { succeeded message } } } }",
                {"path": PAGINA_LACUNAS, **comuns})


# ---------- Open WebUI ----------

def colecoes() -> dict[str, str]:
    """nome -> id das coleções de conhecimento; cria as que faltarem."""
    existentes = http("GET", f"{OWUI_URL}/api/v1/knowledge/", OWUI_API_KEY) or []
    if isinstance(existentes, dict):  # algumas versões paginam
        existentes = existentes.get("items", [])
    ids = {c["name"]: c["id"] for c in existentes}
    for nome, descricao in CAMADAS.values():
        if nome not in ids:
            if SIMULAR:
                ids[nome] = f"simulado-{nome}"
                continue
            nova = http("POST", f"{OWUI_URL}/api/v1/knowledge/create", OWUI_API_KEY,
                        {"name": nome, "description": descricao})
            ids[nome] = nova["id"]
            log(f"coleção criada: {nome}")
    return ids


def enviar_arquivo(nome: str, texto: str) -> str:
    fronteira = uuid.uuid4().hex
    corpo = (f"--{fronteira}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{nome}\"\r\n"
             f"Content-Type: text/markdown\r\n\r\n").encode() + texto.encode() + f"\r\n--{fronteira}--\r\n".encode()
    resp = http("POST", f"{OWUI_URL}/api/v1/files/", OWUI_API_KEY, corpo=corpo,
                tipo=f"multipart/form-data; boundary={fronteira}")
    return resp["id"]


def ligar(colecao_id: str, arquivo_id: str) -> None:
    # O processamento do arquivo pode ser assíncrono: tenta algumas vezes.
    for tentativa in range(10):
        try:
            http("POST", f"{OWUI_URL}/api/v1/knowledge/{colecao_id}/file/add", OWUI_API_KEY, {"file_id": arquivo_id})
            return
        except urllib.error.HTTPError as e:
            if tentativa == 9:
                raise RuntimeError(f"não consegui adicionar {arquivo_id}: {e.code} {e.read()[:200]!r}")
            time.sleep(3)


def desligar(colecao_id: str, arquivo_id: str) -> None:
    try:
        http("POST", f"{OWUI_URL}/api/v1/knowledge/{colecao_id}/file/remove", OWUI_API_KEY, {"file_id": arquivo_id})
    except urllib.error.HTTPError as e:
        log(f"aviso: remoção de {arquivo_id} falhou ({e.code}); seguindo")


# ---------- Lacunas ----------

def resumir_lacunas() -> str | None:
    if not LACUNAS.exists():
        return None
    contagem: Counter = Counter()
    ultima: dict[str, str] = {}
    for linha in LACUNAS.read_text(encoding="utf-8").splitlines():
        try:
            item = json.loads(linha)
        except json.JSONDecodeError:
            continue
        chave = " ".join(item.get("pergunta", "").lower().split())[:300]
        if not chave:
            continue
        contagem[chave] += 1
        ultima[chave] = max(ultima.get(chave, ""), item.get("data", ""))
    if not contagem:
        return None
    linhas = [
        "# Lacunas do acervo",
        "",
        "Perguntas que o assistente não conseguiu responder com o acervo, das mais frequentes para as menos.",
        "**Curadoria:** apague dados pessoais antes de copiar qualquer pergunta para a página pública de lacunas.",
        "",
        "| Vezes | Última vez | Pergunta |",
        "| --- | --- | --- |",
    ]
    for pergunta, vezes in contagem.most_common(200):
        linhas.append(f"| {vezes} | {ultima[pergunta][:10]} | {pergunta.replace('|', '/')} |")
    return "\n".join(linhas)


# ---------- Principal ----------

def main() -> None:
    faltando = [n for n, v in [("WIKI_API_KEY", WIKI_API_KEY), ("OWUI_API_KEY", OWUI_API_KEY)] if not v]
    if faltando:
        log(f"configuração incompleta: {', '.join(faltando)}. Veja docs/pt/04-instalacao.md")
        return

    estado = json.loads(ESTADO.read_text()) if ESTADO.exists() else {}
    ids_colecao = colecoes()
    vistos = set()
    novos = alterados = removidos = 0

    for resumo in listar_paginas():
        camada = camada_de(resumo["path"])
        if not camada or not resumo["isPublished"]:
            continue
        chave = str(resumo["id"])
        vistos.add(chave)
        anterior = estado.get(chave)
        # Reenvia se mudou, ou se uma ficha acabou de ficar vencida
        vencida = camada == "Fichas de solução" and meses_desde(resumo["updatedAt"]) > VALIDADE_MESES
        if anterior and anterior["updatedAt"] == resumo["updatedAt"] and anterior.get("vencida", False) == vencida:
            continue
        pagina = ler_pagina(resumo["id"])
        texto = montar_documento(pagina, camada)
        nome = pagina["path"].replace("/", "__") + ".md"
        if SIMULAR:
            log(f"[simulação] enviaria {nome} -> {camada} ({len(texto)} caracteres)")
            continue
        if anterior:
            desligar(anterior["colecao"], anterior["arquivo"])
            alterados += 1
        else:
            novos += 1
        arquivo_id = enviar_arquivo(nome, texto)
        colecao_id = ids_colecao[camada]
        ligar(colecao_id, arquivo_id)
        estado[chave] = {"updatedAt": resumo["updatedAt"], "arquivo": arquivo_id,
                         "colecao": colecao_id, "caminho": pagina["path"], "vencida": vencida}

    for chave in list(estado):
        if chave not in vistos:
            if not SIMULAR:
                desligar(estado[chave]["colecao"], estado[chave]["arquivo"])
            log(f"removida do acervo do assistente: {estado[chave]['caminho']}")
            del estado[chave]
            removidos += 1

    if not SIMULAR:
        ESTADO.parent.mkdir(parents=True, exist_ok=True)
        ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=1))
    log(f"sincronização concluída: {novos} novas, {alterados} alteradas, {removidos} removidas")

    lacunas = resumir_lacunas()
    if lacunas and not SIMULAR:
        marca = ESTADO.with_name("lacunas.sha256")
        resumo_hash = hashlib.sha256(lacunas.encode()).hexdigest()
        if not marca.exists() or marca.read_text() != resumo_hash:
            publicar_lacunas(lacunas)
            marca.write_text(resumo_hash)
            log("página de lacunas atualizada")


if __name__ == "__main__":
    main()
