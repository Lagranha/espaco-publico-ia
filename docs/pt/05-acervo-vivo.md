# 5. O acervo vivo

> O acervo é o centro do projeto; o assistente é só uma forma de consultá-lo. Ele tem três camadas, cresce com fichas de solução e lacunas, e cada informação carrega sua procedência e sua data.

## As três camadas

| Camada | Caminho na wiki | O que entra | Quem inclui | Como o assistente apresenta |
| --- | --- | --- | --- | --- |
| Documentos oficiais | `oficial/` | Leis municipais, Plano Diretor, atos, cartilhas de serviços públicos | Curadores | "Segundo a Lei X..." |
| Memória local | `memoria/` | Entrevistas, histórias, estudos sobre a cidade | Curadores, com consentimento | "Segundo o relato de moradores do bairro X..." |
| Fichas de solução | `fichas/` | Como moradores resolveram problemas reais | Contribuidores, com revisão | "Um morador conta que..." e o aviso de que é relato |

## Como o acervo cresce

**Fichas de solução.** Quem resolveu um problema escreve uma ficha a partir do [modelo](../../wiki-modelos/ficha-de-solucao.md), em `fichas/rascunhos/`. Um curador revisa: retira dados pessoais, confere se os canais e procedimentos existem, ajusta a linguagem. Depois move a ficha para `fichas/`, e na sincronização seguinte ela entra no assistente. Fichas de tentativas que não deram certo também são valiosas.

**Validade.** Cada ficha tem data. Depois de 12 meses (configurável), o sincronizador acrescenta ao texto o aviso "pode estar desatualizada", e o assistente o repete. Quando alguém confirma que o caminho continua valendo, basta editar a ficha (atualizar a data de verificação) para o aviso sumir.

**Lacunas.** Quando o assistente responde "Não encontrei isso no acervo.", o filtro de lacunas guarda a pergunta, sem nenhum dado de quem perguntou. O sincronizador junta perguntas repetidas e publica a lista, das mais frequentes às menos, na página interna `curadoria/lacunas`. A curadoria revisa, apaga dados pessoais e copia para a página pública `lacunas` as que valem uma busca. Moradores e mediadores ajudam a encontrar as fontes.

**Documentos e memórias.** Entram por iniciativa da curadoria, de parceiros (câmara, arquivo municipal, universidade) ou de pedidos da comunidade, seguindo o critério de entrada abaixo.

## Critério de entrada (aprovado pelo conselho)

Um conteúdo entra no acervo se:

1. tem origem conhecida e confiável;
2. pode ser compartilhado (domínio público, autorização ou consentimento);
3. não expõe dados pessoais de terceiros;
4. é útil para alguém da cidade entender algo ou resolver um problema.

## Papéis

| Papel | Pode | Como se torna |
| --- | --- | --- |
| Leitor | Consultar o assistente e a wiki, comentar | Cadastro aprovado |
| Contribuidor | Escrever fichas em rascunho, sugerir documentos | Pedido ao curador, depois de uma oficina ou de uma primeira ficha aprovada |
| Curador | Aprovar fichas, incluir documentos, tratar lacunas | Indicação do conselho; formação em ética e dados |
| Conselho | Definir regras, licença, provedor de IA | Ver [governança](08-governanca.md) |

## Boas práticas de escrita no acervo

- Um assunto por página: páginas curtas são encontradas com mais precisão pelo assistente.
- Título que diga o que a página responde: "Como pedir poda de árvore", e não "Árvores".
- Sempre a data e a fonte no alto da página.
- Documentos escaneados precisam de OCR antes (`ocrmypdf entrada.pdf saida.pdf -l por`); cole o texto na página e anexe o PDF.
