# 2. Arquitetura

> Um servidor pequeno, sem placa de vídeo, guarda tudo o que é da comunidade: contas, conversas, a wiki e o índice de busca. Só a geração do texto das respostas é feita fora, pela IA pública suíça, por um gateway que esconde quem perguntou.

```
  Moradores (navegador, celular)
        │ HTTPS
        ▼
 ┌──────────────── SERVIDOR DO PROJETO (no Brasil) ────────────────┐
 │                                                                  │
 │  Caddy ── HTTPS, bloqueio de robôs, cabeçalhos "noai"            │
 │    ├── ia.suacidade.org.br      → Open WebUI (assistente)        │
 │    └── acervo.suacidade.org.br  → Wiki.js (acervo vivo)          │
 │                                                                  │
 │  Wiki.js + PostgreSQL ── documentos, memória, fichas, lacunas    │
 │        │ sincronizador (a cada hora)                             │
 │        ▼                                                         │
 │  Open WebUI ── contas, conversas (30 dias), busca no acervo      │
 │     • embeddings bge-m3 calculados AQUI (o acervo não sai)       │
 │     • filtros: registro de lacunas, limite diário                │
 │     • Whisper local para áudio                                   │
 │        │ pergunta + trechos relevantes                           │
 │        ▼                                                         │
 │  Gateway (Caddy :8081) ── injeta a chave, remove IP e cookies    │
 └────────┼─────────────────────────────────────────────────────────┘
          │ HTTPS
          ▼
  Public AI Inference Utility (sem fins lucrativos)
          → modelo Apertus (universidades públicas suíças)
```

## Componentes

| Componente | Software (aberto) | Função |
| --- | --- | --- |
| Porta de entrada | [Caddy](https://caddyserver.com) | HTTPS automático, `robots.txt`, bloqueio de robôs de IA, cabeçalhos de reserva de mineração |
| Gateway da IA | Caddy (bloco interno `:8081`) | Guarda a chave da API, identifica o projeto, remove IP e cookies dos usuários; trocar de provedor = mudar este bloco |
| Assistente | [Open WebUI](https://docs.openwebui.com) | Conversa, contas, grupos, busca no acervo (RAG), transcrição |
| Acervo vivo | [Wiki.js](https://js.wiki) + PostgreSQL | Páginas legíveis, histórico de versões, comentários, permissões por caminho |
| Sincronizador | `tools/sincronizar_acervo.py` | Copia a wiki publicada para a busca do assistente; publica lacunas para a curadoria |
| Faxina | `tools/limpar_conversas.py` | Apaga conversas com mais de 30 dias |
| Modelo | Apertus 1.5 (8B ou 70B), via [Public AI](https://publicai.co) | Gera o texto das respostas |

## O que sai do servidor e o que não sai

| Dado | Sai? |
| --- | --- |
| Acervo inteiro, contas, e-mails, IPs, lista de lacunas | **Não** |
| Embeddings (índice de busca) | **Não**: são calculados no próprio servidor |
| Áudios para transcrição | **Não**: o Whisper roda no servidor |
| Pergunta, histórico da conversa e 3 a 5 trechos do acervo | **Sim**, para o Public AI, a cada resposta |

## Requisitos do servidor

- **Mínimo:** 4 vCPU, 8 GB de RAM, 60 GB de disco (o modelo de embeddings e o Whisper usam 3 a 4 GB de RAM).
- **Recomendado:** 4 a 8 vCPU, 16 GB de RAM.
- **Sem GPU.** Ubuntu 24.04 ou Debian 12, com Docker.
- **Onde:** de preferência numa universidade, instituto federal ou prefeitura parceira; alternativa, um provedor de nuvem brasileiro.

## Por que Wiki.js e Open WebUI separados

A wiki é o acervo **humano**: lido, discutido, corrigido e com histórico. O assistente é só uma forma de consultar. Se um dia o assistente sair do ar, ou o provedor de IA mudar, o acervo continua inteiro e útil. Dois logins são o custo dessa escolha; a fase 2 prevê login único (ver [piloto](09-piloto-e-custos.md)).
