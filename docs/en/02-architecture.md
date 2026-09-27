# 2. Architecture

> A small server with no GPU keeps everything that belongs to the community: accounts, conversations, the wiki and the search index. Only text generation happens outside, on Swiss public AI, through a gateway that hides who asked.

```
  Residents (browser, phone)
        │ HTTPS
        ▼
 ┌──────────────── PROJECT SERVER (in Brazil) ─────────────────────┐
 │                                                                  │
 │  Caddy ── HTTPS, bot blocking, "noai" headers                    │
 │    ├── ia.yourcity.org      → Open WebUI (assistant)             │
 │    └── acervo.yourcity.org  → Wiki.js (living archive)           │
 │                                                                  │
 │  Wiki.js + PostgreSQL ── documents, memory, records, gaps        │
 │        │ sync (hourly)                                           │
 │        ▼                                                         │
 │  Open WebUI ── accounts, conversations (30 days), archive search │
 │     • bge-m3 embeddings computed HERE (archive never leaves)     │
 │     • filters: gap logging, daily limit                          │
 │     • local Whisper for audio                                    │
 │        │ question + relevant passages                            │
 │        ▼                                                         │
 │  Gateway (Caddy :8081) ── injects key, strips IP and cookies     │
 └────────┼─────────────────────────────────────────────────────────┘
          │ HTTPS
          ▼
  Public AI Inference Utility (nonprofit)
          → Apertus model (Swiss public universities)
```

## Components

| Component | Software (open) | Role |
| --- | --- | --- |
| Front door | [Caddy](https://caddyserver.com) | Automatic HTTPS, `robots.txt`, AI-bot blocking, mining-reservation headers |
| AI gateway | Caddy (internal `:8081` block) | Holds the API key, identifies the project, strips users' IPs and cookies; switching provider = editing this block |
| Assistant | [Open WebUI](https://docs.openwebui.com) | Chat, accounts, groups, archive search (RAG), transcription |
| Living archive | [Wiki.js](https://js.wiki) + PostgreSQL | Readable pages, version history, comments, path-based permissions |
| Sync | `tools/sincronizar_acervo.py` | Copies published wiki pages into the assistant's search; publishes gaps for curators |
| Cleanup | `tools/limpar_conversas.py` | Deletes conversations older than 30 days |
| Model | Apertus 1.5 (8B or 70B) via [Public AI](https://publicai.co) | Generates answer text |

## What leaves the server and what doesn't

| Data | Leaves? |
| --- | --- |
| Whole archive, accounts, emails, IPs, gap list | **No** |
| Embeddings (search index) | **No**: computed on the server |
| Audio for transcription | **No**: Whisper runs on the server |
| Question, conversation history and 3–5 archive passages | **Yes**, to Public AI, for each answer |

## Server requirements

- **Minimum:** 4 vCPU, 8 GB RAM, 60 GB disk (the embedding model and Whisper use 3–4 GB RAM).
- **Recommended:** 4–8 vCPU, 16 GB RAM.
- **No GPU.** Ubuntu 24.04 or Debian 12, with Docker.
- **Where:** ideally a partner university, technical institute or city hall; otherwise a national cloud provider.

## Why Wiki.js and Open WebUI are separate

The wiki is the **human** archive: read, discussed, corrected, versioned. The assistant is just one way to consult it. If the assistant goes offline or the AI provider changes, the archive remains whole and useful. Two logins are the cost of this choice; phase 2 plans single sign-on (see [pilot](09-pilot-and-costs.md)).
