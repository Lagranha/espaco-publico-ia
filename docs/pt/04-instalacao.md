# 4. Instalação

> Com um servidor Linux, dois endereços de DNS e uma chave do Public AI, o Espaço fica no ar em uma tarde. A configuração do acervo e da curadoria leva mais alguns dias.

## Antes de começar

- Um servidor com Ubuntu 24.04 ou Debian 12, 4 vCPU, 8 a 16 GB de RAM, IP público ([requisitos](02-arquitetura.md#requisitos-do-servidor)).
- Docker e Docker Compose: `curl -fsSL https://get.docker.com | sh`.
- Dois nomes de domínio apontando para o IP do servidor, ex.: `ia.suacidade.org.br` e `acervo.suacidade.org.br`.
- Portas 80 e 443 abertas.
- Uma chave de API do [Public AI](https://platform.publicai.co) (ver [a IA pública suíça](03-ia-publica-suica.md)).

## 1. Subir os serviços

```bash
git clone https://github.com/<organizacao>/espaco-publico-ia.git
cd espaco-publico-ia/deploy
cp .env.example .env
nano .env        # preencha domínios, e-mails, PUBLICAI_API_KEY, WEBUI_SECRET_KEY, POSTGRES_PASSWORD
docker compose up -d
docker compose logs -f caddy   # acompanhe a emissão dos certificados HTTPS
```

Gere os segredos com `openssl rand -hex 32`.

## 2. Configurar o assistente (Open WebUI)

1. Abra `https://ia.suacidade.org.br` e **crie imediatamente a conta de administrador** (a primeira conta vira admin).
2. *Painel de administração → Configurações → Conexões*: confira se a conexão OpenAI aponta para `http://caddy:8081/v1` e se os modelos `swiss-ai/apertus-...` aparecem. Se a lista vier vazia, adicione os ids de modelo manualmente na conexão.
3. *Configurações → Geral*: cadastro ativado, papel padrão **pendente** (cada conta é aprovada).
4. *Funções → +*: cole [`tools/filtro_lacunas.py`](../../tools/filtro_lacunas.py) e [`tools/filtro_limite.py`](../../tools/filtro_limite.py); ative os dois; marque o de limite como **global**.
5. *Espaço de trabalho → Modelos*: crie o **Assistente do Acervo** com base em `swiss-ai/apertus-v1.5-70b`, o prompt de [`prompts/pt/assistente-acervo.md`](../../prompts/pt/assistente-acervo.md), as três coleções de conhecimento (criadas pelo sincronizador) e o filtro de lacunas ativado. Repita para o Parceiro de Estudo e o Leitor de Documentos.
6. *Usuários → Grupos*: crie grupos para oficinas e instituições parceiras.
7. *Configurações → Conta → Chaves de API*: gere uma chave e coloque em `OWUI_API_KEY` no `.env`.

## 3. Configurar o acervo (Wiki.js)

1. Abra `https://acervo.suacidade.org.br`, crie o administrador e informe o endereço do site.
2. *Administração → Grupos*: configure os grupos e permissões de [`wiki-modelos/README.md`](../../wiki-modelos/README.md). **Tire toda permissão de leitura do grupo Guests**: o acervo não pode ser público.
3. *Administração → Login*: permita autocadastro no grupo **Leitores**, se quiser, ou cadastre as pessoas manualmente.
4. *Administração → API*: ative a API, gere uma chave com acesso total e coloque em `WIKI_API_KEY` no `.env`.
5. Crie as páginas `inicio`, `lacunas`, `licenca`, `termos` e `sobre-a-ia` a partir de [`wiki-modelos/`](../../wiki-modelos/) e [`templates/pt/`](../../templates/pt/).
6. Publique os primeiros documentos em `oficial/` e as primeiras fichas em `fichas/`.

## 4. Ligar a sincronização

```bash
docker compose up -d sincronizador      # recarrega com as chaves novas
docker compose exec sincronizador python /tools/sincronizar_acervo.py --simular
docker compose logs -f sincronizador
```

A simulação lista o que seria enviado sem enviar nada. Depois, a cada hora, as páginas novas ou alteradas vão para o assistente.

## 5. Proteção do acervo

```bash
python tools/canarios.py gerar 10     # rode num computador da curadoria, não no repositório
```

Insira as frases em páginas diferentes do acervo e anote onde, em `canarios.csv`, guardado fora do Git. Veja [proteção do acervo](06-protecao-do-acervo.md).

## 6. Testar antes de abrir

- [ ] Sem login, `https://acervo...` e `https://ia...` não mostram conteúdo algum.
- [ ] `curl -A GPTBot https://acervo.suacidade.org.br/` retorna 403.
- [ ] O assistente responde a uma pergunta do acervo citando a página e a camada.
- [ ] Uma pergunta fora do acervo gera "Não encontrei isso no acervo." e aparece em `curadoria/lacunas` depois da sincronização.
- [ ] Um usuário comum é bloqueado depois do limite diário.
- [ ] O backup funciona: `bash backup.sh /mnt/backup`.

## Manutenção

| Quando | O quê |
| --- | --- |
| Toda semana | Backup (`deploy/backup.sh`); revisar fichas em rascunho e lacunas |
| Todo mês | `docker compose pull && docker compose up -d` (atualizações); conferir o gasto no painel do Public AI |
| Todo trimestre | Rodar o teste de perguntas; procurar os canários em modelos comerciais |
| Todo semestre | Rever os termos do Public AI e o plano de saída |
