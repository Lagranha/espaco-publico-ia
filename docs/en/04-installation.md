# 4. Installation

> With a Linux server, two DNS names and a Public AI key, the Espaço is online in an afternoon. Setting up the archive and curation takes a few more days.

## Before you start

- A server with Ubuntu 24.04 or Debian 12, 4 vCPU, 8–16 GB RAM, public IP ([requirements](02-architecture.md#server-requirements)).
- Docker and Docker Compose: `curl -fsSL https://get.docker.com | sh`.
- Two domain names pointing to the server's IP, e.g. `ia.yourcity.org` and `acervo.yourcity.org`.
- Ports 80 and 443 open.
- A [Public AI](https://platform.publicai.co) API key (see [Swiss public AI](03-swiss-public-ai.md)).

## 1. Start the services

```bash
git clone https://github.com/<organization>/espaco-publico-ia.git
cd espaco-publico-ia/deploy
cp .env.example .env
nano .env        # fill in domains, emails, PUBLICAI_API_KEY, WEBUI_SECRET_KEY, POSTGRES_PASSWORD
docker compose up -d
docker compose logs -f caddy   # watch HTTPS certificates being issued
```

Generate secrets with `openssl rand -hex 32`.

## 2. Configure the assistant (Open WebUI)

1. Open `https://ia.yourcity.org` and **create the admin account right away** (the first account becomes admin).
2. *Admin Panel → Settings → Connections*: check that the OpenAI connection points to `http://caddy:8081/v1` and that `swiss-ai/apertus-...` models are listed. If the list is empty, add the model ids manually in the connection.
3. *Settings → General*: sign-up enabled, default role **pending** (each account is approved).
4. *Functions → +*: paste [`tools/filtro_lacunas.py`](../../tools/filtro_lacunas.py) and [`tools/filtro_limite.py`](../../tools/filtro_limite.py); enable both; mark the limit filter as **global**.
5. *Workspace → Models*: create the **Archive Assistant** based on `swiss-ai/apertus-v1.5-70b`, with the prompt in [`prompts/en/archive-assistant.md`](../../prompts/en/archive-assistant.md), the three knowledge collections (created by the sync) and the gap filter enabled. Repeat for the Study Partner and Document Reader.
6. *Users → Groups*: create groups for workshops and partner institutions.
7. *Settings → Account → API Keys*: generate a key and put it in `OWUI_API_KEY` in `.env`.

## 3. Configure the archive (Wiki.js)

1. Open `https://acervo.yourcity.org`, create the admin and set the site URL.
2. *Administration → Groups*: set groups and permissions from [`wiki-modelos/README.md`](../../wiki-modelos/README.md). **Remove all read permission from the Guests group**: the archive must not be public.
3. *Administration → Login*: allow self-registration into the **Readers** group, or register people manually.
4. *Administration → API*: enable the API, create a full-access key and put it in `WIKI_API_KEY` in `.env`.
5. Create the `inicio`, `lacunas`, `licenca`, `termos` and `sobre-a-ia` pages from [`wiki-modelos/`](../../wiki-modelos/) and [`templates/en/`](../../templates/en/).
6. Publish the first documents under `oficial/` and the first records under `fichas/`.

## 4. Turn on sync

```bash
docker compose up -d sincronizador      # reload with the new keys
docker compose exec sincronizador python /tools/sincronizar_acervo.py --simular
docker compose logs -f sincronizador
```

The dry run lists what would be sent without sending anything. Afterwards, new or changed pages go to the assistant every hour.

## 5. Archive protection

```bash
python tools/canarios.py gerar 10     # run on a curator's computer, not in the repository
```

Insert the phrases into different archive pages and note where in `canarios.csv`, kept outside Git. See [archive protection](06-archive-protection.md).

## 6. Test before opening

- [ ] Without login, `https://acervo...` and `https://ia...` show no content.
- [ ] `curl -A GPTBot https://acervo.yourcity.org/` returns 403.
- [ ] The assistant answers an archive question citing the page and layer.
- [ ] A question outside the archive produces "I could not find this in the archive." and shows up in `curadoria/lacunas` after sync.
- [ ] A regular user is blocked after the daily limit.
- [ ] Backup works: `bash backup.sh /mnt/backup`.

## Maintenance

| When | What |
| --- | --- |
| Weekly | Backup (`deploy/backup.sh`); review draft records and gaps |
| Monthly | `docker compose pull && docker compose up -d` (updates); check spending on the Public AI dashboard |
| Quarterly | Rerun the question test; check canaries in commercial models |
| Every six months | Review Public AI's terms and the exit plan |
