# 6. Proteção do acervo

> Nenhuma medida torna impossível copiar um conteúdo a que pessoas têm acesso. O que o Espaço faz é tornar o uso para treinar IA **difícil, ilegítimo e detectável**, em quatro camadas.

## 1. Camada técnica: difícil

| Medida | Onde está | O que faz |
| --- | --- | --- |
| Tudo atrás de login | Wiki.js (Guests sem leitura) e Open WebUI (contas pendentes) | Robôs de coleta, que não fazem login, não veem nada |
| Bloqueio de robôs de IA conhecidos | `Caddyfile` (`@robos_ia`) | GPTBot, ClaudeBot, CCBot, Google-Extended e outros recebem 403 |
| `robots.txt` restritivo | `deploy/robots.txt` | Declara a proibição para os robôs que respeitam o arquivo |
| Sem exportação em massa | Permissões da wiki; limite diário no assistente | Dificulta copiar o acervo inteiro por dentro |
| Contas aprovadas | `DEFAULT_USER_ROLE=pending` | Cada conta é conferida antes de acessar |

## 2. Camada jurídica: ilegítimo

- **[Licença de Guarda Comunitária](../../templates/pt/licenca-do-acervo.md)**: proíbe expressamente treinar, ajustar ou avaliar modelos de IA com o acervo, e coletá-lo por meios automatizados.
- **Reserva de mineração de texto e dados**, declarada no texto da licença e de forma legível por máquina: cabeçalhos `tdm-reservation: 1` e `X-Robots-Tag: noai`, aplicados pelo Caddy.
- **[Termos de uso](../../templates/pt/termos-de-uso.md)** aceitos no cadastro, repetindo a proibição.

Isso cria base para cobrar quem desrespeitar. O quadro legal brasileiro sobre IA e direitos autorais ainda está em discussão; a reserva expressa é a melhor posição disponível enquanto isso.

## 3. Camada de detecção: detectável

**Frases-canário** ([`tools/canarios.py`](../../tools/canarios.py)): frases inventadas, plausíveis e únicas (nomes de lugares e pessoas que não existem), inseridas em algumas páginas. Se um modelo comercial um dia responder sobre "a enchente do córrego Tobunaba", é forte indício de que o acervo foi copiado.

- Gere 10 a 20, insira cada uma numa página diferente, no meio do texto.
- Guarde a lista (`canarios.csv`) **fora do repositório** e fora da wiki.
- Uma vez por trimestre, pergunte aos principais modelos comerciais sobre os canários (`canarios.py perguntas`) e verifique as respostas (`canarios.py verificar`).
- Avise os curadores onde estão, para que não sejam "corrigidos".

## 4. Camada do próprio assistente: não vazar pelo uso

O assistente é, ele mesmo, um caminho de saída do acervo: cada resposta envia trechos ao provedor de IA. Por isso:

- só o **Public AI**, com termos que proíbem treinar com os dados, e sem aderir ao programa voluntário de doação de dados;
- **embeddings calculados no servidor**: o acervo nunca é enviado inteiro para indexação;
- **gateway** que não repassa quem perguntou;
- pedido formal ao Public AI de exclusão do compartilhamento com pesquisadores (ver [a IA pública suíça](03-ia-publica-suica.md#as-ressalvas-com-franqueza)).

## O que isto não resolve

Uma pessoa cadastrada pode copiar páginas à mão e publicá-las em outro lugar, de onde um robô as coletaria. A resposta a isso é social e jurídica: cultura de cuidado com o acervo, licença clara, canários para provar a origem. Conteúdo que não pode correr esse risco de jeito nenhum não deve entrar no acervo.
