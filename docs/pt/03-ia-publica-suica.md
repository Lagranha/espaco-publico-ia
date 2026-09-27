# 3. A IA pública suíça: Apertus e Public AI

> O Espaço usa o **Apertus**, modelo aberto das universidades públicas suíças, por meio do **Public AI Inference Utility**, um serviço sem fins lucrativos com API compatível com o padrão OpenAI. É barato, mas não é gratuito, e não é livre de big techs: é a opção de **menor dependência viável** hoje, com as ressalvas abaixo. Informações conferidas em setembro de 2026.

## Por que o Apertus

- **Criado por instituições públicas:** Swiss AI Initiative, com EPFL, ETH Zurique e o centro nacional de supercomputação suíço (CSCS).
- **Aberto de verdade:** pesos, código **e dados de treino** abertos, o que é raro. Dá para saber o que o modelo leu.
- **Multilíngue:** treinado com muitas línguas. **Teste em português** com as perguntas da sua comunidade antes de decidir (`tools/avaliar_modelos.py`).
- **Pode rodar em qualquer lugar:** se o Public AI deixar de existir, o mesmo modelo pode ser rodado numa universidade brasileira.

## O serviço: Public AI Inference Utility

| Item | Situação (setembro de 2026) |
| --- | --- |
| O que é | Serviço sem fins lucrativos e de código aberto para dar acesso a modelos públicos |
| API | `https://api.publicai.co/v1`, compatível com OpenAI (`/chat/completions`); exige chave e cabeçalho `User-Agent` |
| Chave | Cadastro em [platform.publicai.co](https://platform.publicai.co), seção API Keys |
| Custo | Por token; **US$ 2 de crédito inicial**; depois, recarga ou contribuição via OpenCollective |
| Limite de requisições | Gratuito: 100 por minuto; Plus: 200; Pro: 300 |
| Embeddings | Não oferece: por isso o Espaço calcula os embeddings no próprio servidor |

### Modelos e preços (por milhão de tokens)

| Modelo | Contexto | Entrada | Saída | Uso sugerido |
| --- | --- | --- | --- | --- |
| `swiss-ai/apertus-v1.5-8b` | 262 mil | US$ 0,10 | US$ 0,20 | Tarefas internas; testes; conversas se o orçamento for muito curto |
| `swiss-ai/apertus-v1.5-70b` | 262 mil | US$ 0,82 | US$ 2,92 | Conversas com os moradores (padrão) |

Fonte: [catálogo de modelos do Public AI](https://platform.publicai.co/models). Preços mudam: confira antes de orçar.

### Quanto custa por pergunta

Uma pergunta típica ao acervo envia cerca de 2.500 tokens (instruções, trechos do acervo, histórico) e recebe cerca de 400.

| Modelo | Custo por pergunta | 10 mil perguntas por mês |
| --- | --- | --- |
| Apertus 70B | ≈ US$ 0,003 | ≈ US$ 32 |
| Apertus 8B | ≈ US$ 0,0003 | ≈ US$ 3 |

Estimativa aproximada; meça o consumo real com `tools/avaliar_modelos.py`, que registra os tokens.

## As ressalvas, com franqueza

Os [termos do Public AI](https://publicai.co/tc) dizem que:

1. **Não usa os dados para treinar modelos**, exceto de quem aderir a um programa voluntário ("Data Flywheel"). O Espaço **não deve aderir**.
2. **Guarda registros técnicos por até 90 dias.**
3. **Pode compartilhar conversas com pesquisadores acadêmicos**, sob acordos de uso, para pesquisa não comercial.
4. **Usa parceiros de computação**: o CSCS (público suíço), a Exoscale (nuvem suíça) e a **Amazon Web Services**, entre outros, e declara **não controlar** o que esses parceiros fazem com os dados.
5. É regido pelas leis de Massachusetts (EUA), exige usuários com **18 anos ou mais** e se apresenta como voltado a **pesquisa e educação**; proíbe uso em campanhas políticas.

**O que isso significa para o Espaço:** o acervo inteiro nunca sai do servidor, mas trechos dele e as perguntas passam pelo Public AI e, possivelmente, por um parceiro comercial. Por isso:

- oriente os usuários a **não escrever dados pessoais** nas perguntas;
- não coloque no acervo nada que não possa, em último caso, ser visto por terceiros;
- **escreva ao Public AI** apresentando o projeto e peça: (a) um acordo institucional ou de processamento de dados; (b) a exclusão das conversas do compartilhamento com pesquisadores; (c) roteamento preferencial para a infraestrutura do CSCS; (d) confirmação de que o uso por um serviço público com usuários mediados é compatível com os termos;
- registre a resposta nas atas do conselho e revise a escolha a cada semestre.

## Plano de saída (trocar de provedor em um dia)

O gateway concentra a troca: basta mudar o bloco `:8081` do `Caddyfile` e o nome do modelo no `.env`. Alternativas, da menor para a maior dependência:

1. **Universidade brasileira rodando o Apertus** (ou outro modelo aberto) com vLLM ou Ollama numa GPU própria: zero big tech. É o destino de longo prazo.
2. **Provedor de nuvem brasileiro com GPU**, rodando o mesmo modelo aberto.
3. **Outro provedor de inferência** de modelos abertos, com contrato de não retenção.

Como o Apertus é aberto, a troca não muda o comportamento do assistente.
