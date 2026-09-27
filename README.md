# Espaço Público IA

**[Português](#português) · [English](#english)**

---

## Português

Um **acervo vivo da cidade**, online e gratuito, com um assistente de inteligência artificial que responde a partir dele. O acervo cresce com o que os moradores resolvem, é protegido contra o uso para treinar IAs comerciais, e a IA vem de **infraestrutura pública suíça emprestada**: o modelo aberto **Apertus**, das universidades públicas suíças, por meio do serviço sem fins lucrativos **Public AI**.

É a versão online do [Laboratório Público de IA](https://github.com/Lagranha/laboratorio-publico-ia). A inspiração é uma sugestão do pesquisador Evgeny Morozov: instituições intermediárias, como as bibliotecas públicas, que ofereçam IA como infraestrutura pública, e não como serviço cobrado por uso.

### Como funciona

- **Acervo em três camadas:** documentos oficiais, memória local e **fichas de solução** (como moradores resolveram problemas reais). O assistente sempre diz de qual camada vem cada informação.
- **Acervo que cresce:** quem resolve um problema escreve uma ficha; perguntas sem resposta viram **lacunas** que a comunidade ajuda a preencher.
- **Acervo protegido:** tudo atrás de login, licença de guarda comunitária que proíbe treinar IA com o conteúdo, bloqueio de robôs e **frases-canário** para detectar uso indevido.
- **IA pública, dependência mínima:** o acervo, as contas e o índice de busca ficam no servidor do projeto; só a pergunta e os trechos necessários vão para a IA suíça, sem identificar quem perguntou.
- **Consciência crítica em casa:** atividades de checagem e leitura crítica que também melhoram o acervo, e uma roda online mensal.

```
navegador → Caddy (HTTPS, anti-robôs) → Open WebUI (assistente) + Wiki.js (acervo)
                                            │ pergunta + trechos, sem identificação
                                            ▼
                         gateway → Public AI (sem fins lucrativos) → Apertus
```

### O que tem aqui

| Pasta | Conteúdo |
| --- | --- |
| [`docs/pt/`](docs/pt/) | Proposta, arquitetura, a IA pública suíça, instalação, acervo vivo, proteção, atividades, governança, piloto e custos |
| [`deploy/`](deploy/) | `docker-compose.yml`, `Caddyfile` (com o gateway), `robots.txt`, `.env.example`, backup |
| [`tools/`](tools/) | Sincronização wiki→assistente, filtros de lacunas e de limite diário, faxina de conversas, canários, avaliação de modelos |
| [`prompts/pt/`](prompts/pt/) | Instruções dos assistentes |
| [`wiki-modelos/`](wiki-modelos/) | Estrutura da wiki, modelo de ficha de solução, página inicial, lacunas |
| [`templates/pt/`](templates/pt/) | Licença do acervo, termos de uso, política de dados, termo de consentimento |

### Comece por aqui

1. [Proposta](docs/pt/01-proposta.md) e [a IA pública suíça](docs/pt/03-ia-publica-suica.md), com as ressalvas.
2. [Instalação](docs/pt/04-instalacao.md): um servidor sem GPU, dois domínios e uma chave do Public AI.
3. [Piloto de 12 semanas](docs/pt/09-piloto-e-custos.md).

### Estado do projeto

Protótipo documentado. Os scripts foram testados contra servidores simulados; **teste contra as versões reais antes de um piloto**. Contribuições e relatos de uso são bem-vindos: veja [CONTRIBUTING.md](CONTRIBUTING.md).

### Licença

Código sob [MIT](LICENSE). Documentação sob [CC BY-SA 4.0](LICENSE-docs.md). O **acervo** de cada cidade segue a sua própria [Licença de Guarda Comunitária](templates/pt/licenca-do-acervo.md).

---

## English

A **living archive of the city**, online and free, with an AI assistant that answers from it. The archive grows with what residents solve, is protected against use for training commercial AI, and the AI comes from **borrowed Swiss public infrastructure**: the open model **Apertus**, by Swiss public universities, through the nonprofit **Public AI** service.

It is the online version of the [Laboratório Público de IA](https://github.com/Lagranha/laboratorio-publico-ia). The inspiration is a suggestion by researcher Evgeny Morozov: intermediary institutions, like public libraries, that offer AI as public infrastructure rather than a pay-per-use service.

### How it works

- **A three-layer archive:** official documents, local memory and **solution records** (how residents solved real problems). The assistant always says which layer each piece of information comes from.
- **An archive that grows:** whoever solves a problem writes a record; unanswered questions become **gaps** the community helps fill.
- **A protected archive:** everything behind login, a community guardianship license forbidding AI training on the content, bot blocking and **canary phrases** to detect misuse.
- **Public AI, minimal dependence:** archive, accounts and search index stay on the project's server; only the question and needed passages go to the Swiss AI, without identifying who asked.
- **Critical awareness from home:** checking and critical-reading activities that also improve the archive, plus a monthly online circle.

### What's here

| Folder | Contents |
| --- | --- |
| [`docs/en/`](docs/en/) | Proposal, architecture, Swiss public AI, installation, living archive, protection, activities, governance, pilot and costs |
| [`deploy/`](deploy/) | `docker-compose.yml`, `Caddyfile` (with the gateway), `robots.txt`, `.env.example`, backup |
| [`tools/`](tools/) | Wiki→assistant sync, gap and daily-limit filters, conversation cleanup, canaries, model evaluation |
| [`prompts/en/`](prompts/en/) | Assistant instructions |
| [`wiki-modelos/`](wiki-modelos/) | Wiki structure, solution record template, home page, gaps |
| [`templates/en/`](templates/en/) | Archive license, terms of use, data policy, consent form |

### Start here

1. [Proposal](docs/en/01-proposal.md) and [Swiss public AI](docs/en/03-swiss-public-ai.md), with its caveats.
2. [Installation](docs/en/04-installation.md): a server without GPU, two domains and a Public AI key.
3. [12-week pilot](docs/en/09-pilot-and-costs.md).

### Project status

Documented prototype. Scripts were tested against mock servers; **test against real versions before a pilot**. Contributions and field reports are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).

### License

Code under [MIT](LICENSE). Documentation under [CC BY-SA 4.0](LICENSE-docs.md). Each city's **archive** follows its own [Community Guardianship License](templates/en/archive-license.md).
