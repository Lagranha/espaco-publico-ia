# Ferramentas · Tools

| Arquivo | O que faz | Onde roda |
| --- | --- | --- |
| [`sincronizar_acervo.py`](sincronizar_acervo.py) | Copia as páginas publicadas da wiki (`oficial/`, `memoria/`, `fichas/`) para o acervo pesquisável do assistente; marca fichas vencidas; publica a lista interna de lacunas | Serviço `sincronizador`, a cada hora |
| [`filtro_lacunas.py`](filtro_lacunas.py) | Filtro do Open WebUI: quando o assistente diz "Não encontrei isso no acervo", guarda a pergunta, sem dados do usuário | Dentro do Open WebUI (instale em *Funções*) |
| [`filtro_limite.py`](filtro_limite.py) | Filtro do Open WebUI: limite diário de perguntas por pessoa | Dentro do Open WebUI (instale em *Funções*, marque como global) |
| [`limpar_conversas.py`](limpar_conversas.py) | Apaga conversas com mais de 30 dias | Serviço `faxina`, uma vez por dia |
| [`canarios.py`](canarios.py) | Gera frases-canário para inserir no acervo e verifica se aparecem em respostas de outros modelos | Manualmente, pela curadoria |
| [`avaliar_modelos.py`](avaliar_modelos.py) | Avaliação às cegas de modelos (ex.: Apertus 8B × 70B) com perguntas reais, e contagem de tokens para estimar custo | Manualmente |

Todas usam só a biblioteca padrão do Python, exceto os filtros, que usam o `pydantic` já presente no Open WebUI.

All tools use only the Python standard library, except the filters, which use the `pydantic` already bundled with Open WebUI.

## Testes feitos · Tests done

Os scripts foram testados contra servidores simulados que imitam as APIs do Wiki.js, do Open WebUI e do Public AI. **Antes do piloto, teste contra as versões reais instaladas**: as APIs do Open WebUI mudam com frequência. Rode primeiro `python tools/sincronizar_acervo.py --simular`.

Scripts were tested against mock servers imitating the Wiki.js, Open WebUI and Public AI APIs. **Test against the real installed versions before a pilot**: Open WebUI's APIs change often.
