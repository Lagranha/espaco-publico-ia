"""
title: Limite diário de perguntas
author: Espaço Público IA
version: 1.0
license: MIT
description: Limita o número de perguntas por pessoa por dia, para manter o serviço gratuito
  e o custo previsível. Administradores não têm limite.

Como instalar: Open WebUI -> Painel de administração -> Funções -> "+" -> cole -> salvar ->
ative e marque como "Global" (vale para todos os assistentes).

Os contadores ficam num arquivo, com o id do usuário transformado em hash (não reversível),
e só guardam a contagem do dia.
"""

import hashlib
import json
from datetime import date
from pathlib import Path

from pydantic import BaseModel, Field


class Filter:
    class Valves(BaseModel):
        limite_diario: int = Field(default=30, description="Perguntas por pessoa por dia")
        arquivo: str = Field(default="/app/backend/data/limites/contagem.json")
        mensagem: str = Field(
            default="Você atingiu o limite de {limite} perguntas de hoje. O limite existe para manter o "
            "serviço gratuito para todos. Volte amanhã, ou use o acervo diretamente na wiki."
        )

    def __init__(self):
        self.valves = self.Valves()

    def inlet(self, body: dict, __user__: dict | None = None) -> dict:
        if not __user__ or __user__.get("role") == "admin":
            return body
        caminho = Path(self.valves.arquivo)
        hoje = date.today().isoformat()
        try:
            dados = json.loads(caminho.read_text()) if caminho.exists() else {}
        except (OSError, json.JSONDecodeError):
            dados = {}
        if dados.get("dia") != hoje:
            dados = {"dia": hoje, "contagem": {}}
        chave = hashlib.sha256(str(__user__.get("id", "")).encode()).hexdigest()[:16]
        usados = dados["contagem"].get(chave, 0)
        if usados >= self.valves.limite_diario:
            raise Exception(self.valves.mensagem.format(limite=self.valves.limite_diario))
        dados["contagem"][chave] = usados + 1
        try:
            caminho.parent.mkdir(parents=True, exist_ok=True)
            caminho.write_text(json.dumps(dados))
        except OSError as erro:
            print(f"[filtro_limite] não consegui gravar a contagem: {erro}")
        return body
