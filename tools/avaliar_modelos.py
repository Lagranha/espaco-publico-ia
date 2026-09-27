#!/usr/bin/env python3
"""
Avaliação de modelos com perguntas da comunidade / model evaluation with community questions.

Envia as mesmas perguntas a vários modelos de uma API compatível com OpenAI
(por padrão, a IA pública suíça: api.publicai.co) e gera uma planilha para
avaliação ÀS CEGAS: os mediadores veem "Resposta A, B, C" sem saber qual modelo
respondeu. A chave fica num arquivo separado. Também registra tokens gastos,
para estimar o custo.

Só usa a biblioteca padrão do Python (nenhuma instalação extra).

Uso / usage:
    export PUBLICAI_API_KEY=...   # chave criada em platform.publicai.co
    python tools/avaliar_modelos.py perguntas.csv swiss-ai/apertus-v1.5-8b swiss-ai/apertus-v1.5-70b
    python tools/avaliar_modelos.py perguntas.csv swiss-ai/apertus-v1.5-70b --sistema prompts/pt/assistente-acervo.md
    # outra API compatível (ex.: Ollama local): --base-url http://localhost:11434/v1

Saída / output:
    avaliacao-<data>/respostas_para_avaliar.csv   (para os mediadores / for reviewers)
    avaliacao-<data>/chave.csv                    (qual letra é qual modelo / answer key)
    avaliacao-<data>/tempos.csv                   (tempo de resposta / response time)

Depois de avaliar, some as notas por letra e abra a chave.
"""

import argparse
import csv
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

LETRAS = "ABCDEFGH"


def perguntar(base: str, chave: str, modelo: str, pergunta: str, sistema: str | None,
              timeout: int) -> tuple[str, float, int, int]:
    mensagens = []
    if sistema:
        mensagens.append({"role": "system", "content": sistema})
    mensagens.append({"role": "user", "content": pergunta})
    corpo = json.dumps({"model": modelo, "messages": mensagens, "stream": False}).encode()
    cabecalhos = {"Content-Type": "application/json", "User-Agent": "EspacoPublicoIA-avaliacao/1.0"}
    if chave:
        cabecalhos["Authorization"] = f"Bearer {chave}"
    req = urllib.request.Request(f"{base}/chat/completions", data=corpo, headers=cabecalhos)
    inicio = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        dados = json.loads(r.read())
    uso = dados.get("usage") or {}
    texto = dados["choices"][0]["message"]["content"].strip()
    return texto, time.time() - inicio, uso.get("prompt_tokens", 0), uso.get("completion_tokens", 0)


def ler_perguntas(caminho: Path) -> list[dict]:
    with caminho.open(encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    if not linhas or "pergunta" not in linhas[0]:
        sys.exit("O CSV precisa de uma coluna 'pergunta' / the CSV needs a 'pergunta' column.")
    return [l for l in linhas if l["pergunta"].strip()]


def main() -> None:
    p = argparse.ArgumentParser(description="Avaliação às cegas de modelos (API compatível com OpenAI).")
    p.add_argument("perguntas", type=Path, help="CSV com coluna 'pergunta' (e opcionalmente 'categoria')")
    p.add_argument("modelos", nargs="+", help="um ou mais ids de modelo, ex.: swiss-ai/apertus-v1.5-70b")
    p.add_argument("--sistema", type=Path, help="arquivo com prompt de sistema (opcional)")
    p.add_argument("--base-url", default="https://api.publicai.co/v1")
    p.add_argument("--chave-env", default="PUBLICAI_API_KEY", help="variável de ambiente com a chave")
    p.add_argument("--timeout", type=int, default=600)
    p.add_argument("--semente", type=int, default=None, help="semente do sorteio (reprodutibilidade)")
    args = p.parse_args()

    if len(args.modelos) > len(LETRAS):
        sys.exit(f"No máximo {len(LETRAS)} modelos.")

    sistema = args.sistema.read_text(encoding="utf-8") if args.sistema else None
    perguntas = ler_perguntas(args.perguntas)

    base = args.base_url.rstrip("/")
    api_chave = os.environ.get(args.chave_env, "")
    if not api_chave and "publicai" in base:
        sys.exit(f"Defina a chave: export {args.chave_env}=... (crie em https://platform.publicai.co)")

    rng = random.Random(args.semente)
    letras = list(LETRAS[: len(args.modelos)])
    rng.shuffle(letras)
    chave = dict(zip(args.modelos, letras))

    pasta = Path(f"avaliacao-{datetime.now():%Y-%m-%d-%H%M}")
    pasta.mkdir()

    resultados: dict[int, dict[str, str]] = {}
    tempos = []
    total = len(perguntas) * len(args.modelos)
    feito = 0
    for modelo in args.modelos:
        for i, linha in enumerate(perguntas):
            feito += 1
            print(f"[{feito}/{total}] {modelo}: {linha['pergunta'][:60]}…", flush=True)
            try:
                resposta, seg, tk_in, tk_out = perguntar(base, api_chave, modelo, linha["pergunta"],
                                                         sistema, args.timeout)
            except Exception as e:  # registra o erro e segue
                resposta, seg, tk_in, tk_out = f"[ERRO: {e}]", -1.0, 0, 0
            resultados.setdefault(i, {})[chave[modelo]] = resposta
            tempos.append({"modelo": modelo, "pergunta_n": i + 1, "segundos": round(seg, 1),
                           "tokens_entrada": tk_in, "tokens_saida": tk_out})

    ordem = sorted(letras)
    with (pasta / "respostas_para_avaliar.csv").open("w", encoding="utf-8-sig", newline="") as f:
        campos = ["n", "categoria", "pergunta"]
        for l in ordem:
            campos += [f"resposta_{l}", f"nota_{l} (0-3)", f"fonte_correta_{l} (s/n)"]
        campos.append("comentarios")
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for i, linha in enumerate(perguntas):
            reg = {"n": i + 1, "categoria": linha.get("categoria", ""), "pergunta": linha["pergunta"]}
            for l in ordem:
                reg[f"resposta_{l}"] = resultados[i][l]
            w.writerow(reg)

    with (pasta / "chave.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["letra", "modelo"])
        for modelo, letra in sorted(chave.items(), key=lambda x: x[1]):
            w.writerow([letra, modelo])

    with (pasta / "tempos.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["modelo", "pergunta_n", "segundos", "tokens_entrada", "tokens_saida"])
        w.writeheader()
        w.writerows(tempos)

    print(f"\nPronto. Entregue '{pasta}/respostas_para_avaliar.csv' aos mediadores.")
    print("Guarde 'chave.csv' até terminarem a avaliação.")
    for modelo in args.modelos:
        ts = [t["segundos"] for t in tempos if t["modelo"] == modelo and t["segundos"] >= 0]
        if ts:
            tin = sum(t["tokens_entrada"] for t in tempos if t["modelo"] == modelo)
            tout = sum(t["tokens_saida"] for t in tempos if t["modelo"] == modelo)
            print(f"  resposta {chave[modelo]}: tempo médio {sum(ts) / len(ts):.1f} s; "
                  f"tokens: {tin} entrada, {tout} saída (use para estimar o custo por pergunta)")


if __name__ == "__main__":
    main()
