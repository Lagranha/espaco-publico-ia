"""
title: Registro de lacunas do acervo
author: Espaço Público IA
version: 1.0
license: MIT
description: Quando o assistente responde que não encontrou algo no acervo, guarda a pergunta
  (sem nenhum dado do usuário) para que curadores vejam o que falta no acervo.

Como instalar / how to install:
  Open WebUI -> Painel de administração -> Funções -> "+" -> cole este arquivo -> salvar -> ativar.
  Depois, em Espaço de trabalho -> Modelos, ative o filtro nos assistentes do acervo.

O arquivo gerado fica em /app/backend/data/lacunas/lacunas.jsonl e é lido pelo
tools/sincronizar_acervo.py, que publica um resumo na página "curadoria/lacunas" da wiki.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field


class Filter:
    class Valves(BaseModel):
        frases_gatilho: str = Field(
            default="Não encontrei isso no acervo|I could not find this in the archive",
            description="Frases que indicam lacuna, separadas por |. Devem estar nos prompts dos assistentes.",
        )
        arquivo: str = Field(default="/app/backend/data/lacunas/lacunas.jsonl")
        tamanho_maximo: int = Field(default=500, description="Caracteres guardados de cada pergunta")

    def __init__(self):
        self.valves = self.Valves()

    def outlet(self, body: dict, __user__: dict | None = None) -> dict:
        try:
            mensagens = body.get("messages") or []
            if len(mensagens) < 2:
                return body
            resposta = mensagens[-1]
            if resposta.get("role") != "assistant":
                return body
            texto = str(resposta.get("content", ""))
            gatilhos = [g.strip().lower() for g in self.valves.frases_gatilho.split("|") if g.strip()]
            if not any(g in texto.lower() for g in gatilhos):
                return body
            pergunta = next(
                (str(m.get("content", "")) for m in reversed(mensagens[:-1]) if m.get("role") == "user"), ""
            )
            if not pergunta:
                return body
            registro = {
                "data": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "pergunta": pergunta[: self.valves.tamanho_maximo],
                "assistente": body.get("model", ""),
                # De propósito: nenhum nome, e-mail ou id de usuário.
            }
            caminho = Path(self.valves.arquivo)
            caminho.parent.mkdir(parents=True, exist_ok=True)
            with caminho.open("a", encoding="utf-8") as f:
                f.write(json.dumps(registro, ensure_ascii=False) + "\n")
        except Exception as erro:  # o filtro nunca pode quebrar a conversa
            print(f"[filtro_lacunas] erro ignorado: {erro}")
        return body
