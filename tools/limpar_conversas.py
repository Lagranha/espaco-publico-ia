#!/usr/bin/env python3
"""
Apaga conversas do assistente mais antigas que N dias (padrão: 30), como prometido
na política de dados. / Deletes assistant conversations older than N days.

Atua direto no banco SQLite do Open WebUI (webui.db). Confere se a tabela e as colunas
esperadas existem antes de apagar; se o formato mudar numa versão futura, não faz nada.
Conversas marcadas como "arquivadas" ou "fixadas" pelo usuário também são apagadas
após o prazo: a regra é igual para todos.

Uso / usage:
    python tools/limpar_conversas.py /caminho/webui.db [--dias 30] [--simular]
No docker-compose, o serviço "faxina" roda isto uma vez por dia.
"""

import argparse
import sqlite3
import sys
import time


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("banco")
    p.add_argument("--dias", type=int, default=30)
    p.add_argument("--simular", action="store_true")
    a = p.parse_args()

    limite = int(time.time()) - a.dias * 86400
    con = sqlite3.connect(a.banco, timeout=30)
    colunas = {linha[1] for linha in con.execute("PRAGMA table_info(chat)")}
    if not {"id", "updated_at"} <= colunas:
        sys.exit("Tabela 'chat' com formato inesperado: nada foi apagado. Verifique a versão do Open WebUI.")

    # updated_at pode estar em segundos ou nanossegundos, conforme a versão
    maior = con.execute("SELECT MAX(updated_at) FROM chat").fetchone()[0] or 0
    fator = 1_000_000_000 if maior > 10**14 else 1
    antigas = con.execute("SELECT COUNT(*) FROM chat WHERE updated_at < ?", (limite * fator,)).fetchone()[0]

    if a.simular:
        print(f"[simulação] {antigas} conversas com mais de {a.dias} dias seriam apagadas")
        return
    con.execute("DELETE FROM chat WHERE updated_at < ?", (limite * fator,))
    con.commit()
    print(f"{antigas} conversas com mais de {a.dias} dias apagadas")


if __name__ == "__main__":
    main()
