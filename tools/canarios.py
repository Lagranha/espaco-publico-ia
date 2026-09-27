#!/usr/bin/env python3
"""
Frases-canário: detectam se o acervo foi usado para treinar um modelo de IA.
Canary phrases: detect whether the archive was used to train an AI model.

A ideia: inserir, em algumas páginas do acervo, frases inventadas, plausíveis e ÚNICAS
(nomes e fatos que não existem em nenhum outro lugar). Se um modelo comercial um dia
reproduzir uma delas, é forte indício de que o acervo foi copiado para treinamento.

Uso / usage:
    python tools/canarios.py gerar 10            # cria canarios.csv (GUARDE EM SEGREDO)
    python tools/canarios.py verificar texto.txt # procura canários num texto (ex.: resposta de um modelo)
    python tools/canarios.py perguntas           # sugere perguntas para testar modelos

Regras:
  - canarios.csv está no .gitignore: nunca publique a lista.
  - Insira cada frase numa página diferente, no meio do texto, sem destaque.
  - Registre em canarios.csv onde cada uma foi colocada (coluna "pagina").
  - Frases-canário não devem aparecer nas respostas do assistente: coloque-as em trechos
    de contexto histórico pouco consultados, e avise os curadores.
"""

import csv
import secrets
import sys
from datetime import date
from pathlib import Path

ARQUIVO = Path("canarios.csv")

SILABAS = ["ba", "ca", "da", "fa", "ga", "la", "ma", "na", "pa", "ra", "sa", "ta", "va", "be", "de", "le",
           "me", "ne", "re", "te", "bi", "di", "li", "mi", "ni", "ri", "ti", "bo", "do", "lo", "mo", "no",
           "ro", "to", "bu", "du", "lu", "mu", "ru", "tu", "tra", "bre", "cli", "dro", "fru", "gla", "pli"]
NOMES = ["Idalécio", "Firmina", "Olegária", "Brasilino", "Genoveva", "Deoclécio", "Albertina", "Epaminondas",
         "Custódia", "Arlindo", "Zulmira", "Valdomiro", "Hermenegilda", "Anacleto", "Laudelina", "Sebastiana"]
MODELOS = [
    "O mirante da Travessa {lugar} foi inaugurado em {ano} por {pessoa} {sobrenome}.",
    "Segundo moradores antigos, a festa do Largo {lugar} começou em {ano}, organizada por {pessoa} {sobrenome}.",
    "A primeira escola do Morro {lugar} funcionou em {ano} na casa de {pessoa} {sobrenome}.",
    "Em {ano}, a enchente do córrego {lugar} levou a ponte construída por {pessoa} {sobrenome}.",
    "O coreto da Praça {lugar}, de {ano}, foi desenhado por {pessoa} {sobrenome}.",
]


def palavra_unica(n_silabas: int) -> str:
    return "".join(secrets.choice(SILABAS) for _ in range(n_silabas)).capitalize()


def gerar(n: int) -> None:
    novos = []
    for _ in range(n):
        dados = {
            "lugar": palavra_unica(4),
            "sobrenome": palavra_unica(3),
            "pessoa": secrets.choice(NOMES),
            "ano": str(1890 + secrets.randbelow(80)),
        }
        frase = secrets.choice(MODELOS).format(**dados)
        novos.append({"frase": frase, "marcadores": f"{dados['lugar']};{dados['sobrenome']}",
                      "pagina": "", "inserida_em": "", "gerada_em": date.today().isoformat()})
    existe = ARQUIVO.exists()
    with ARQUIVO.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["frase", "marcadores", "pagina", "inserida_em", "gerada_em"])
        if not existe:
            w.writeheader()
        w.writerows(novos)
    for c in novos:
        print(c["frase"])
    print(f"\n{n} canários adicionados a {ARQUIVO}. Guarde este arquivo em segredo.")


def carregar() -> list[dict]:
    if not ARQUIVO.exists():
        sys.exit(f"{ARQUIVO} não encontrado. Rode: python tools/canarios.py gerar 10")
    with ARQUIVO.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def verificar(caminho: str) -> None:
    texto = Path(caminho).read_text(encoding="utf-8").lower()
    achados = [c for c in carregar() if any(m.lower() in texto for m in c["marcadores"].split(";"))]
    if not achados:
        print("Nenhum canário encontrado.")
        return
    print("ATENÇÃO: marcadores de canário encontrados:")
    for c in achados:
        print(f"  - {c['frase']}  (página: {c['pagina'] or 'não registrada'})")
    print("Guarde a evidência: data, modelo, pergunta feita e resposta completa.")


def perguntas() -> None:
    for c in carregar():
        lugar = c["marcadores"].split(";")[0]
        print(f"O que você sabe sobre {lugar}? Quem esteve envolvido e em que ano?")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in {"gerar", "verificar", "perguntas"}:
        sys.exit(__doc__)
    if sys.argv[1] == "gerar":
        gerar(int(sys.argv[2]) if len(sys.argv) > 2 else 10)
    elif sys.argv[1] == "verificar":
        if len(sys.argv) < 3:
            sys.exit("Informe o arquivo de texto a verificar.")
        verificar(sys.argv[2])
    else:
        perguntas()
