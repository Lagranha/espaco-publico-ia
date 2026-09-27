# 10. Ecologia de experimentos

> O Espaço não é uma receita pronta, é um ponto de partida para testar formas diferentes de conviver com a IA. Cada espaço roda experimentos curtos, observa o que as pessoas passaram a conseguir fazer, e decide manter, modificar ou abandonar. Abandonar é um resultado legítimo.

## Por quê

Não dá para decidir de antemão, numa reunião, tudo o que uma tecnologia como a IA deveria ser. Os usos e os próprios valores aparecem na prática: é usando que um grupo descobre se uma ferramenta parece cuidado ou vigilância, se convida a aprender ou a pegar atalhos. Regras fixadas antes e aplicadas de fora tendem a virar uma lista de itens a cumprir, sem ligação com o que acontece de fato.

A ideia vem de um ensaio de Evgeny Morozov (*Nueva Sociedad* nº 323, 2026): em vez de perguntar só "como governar a IA?", perguntar **"que instituições permitem explorar, de forma organizada, diferentes arranjos tecnológicos e diferentes maneiras de viver com eles?"**. A resposta não é um modelo único, mas uma ecologia de experimentos locais: municipais, escolares, comunitários, cada um com suas prioridades, com recursos reais e liberdade para mudar de rumo.

Ele observa também que a interface de conversa, que faz o modelo parecer um interlocutor e não uma biblioteca, foi uma decisão de produto para gerar uso e apego. Alguns experimentos abaixo testam justamente o contrário.

## Princípios

1. **Ciclos curtos:** de 4 a 6 semanas, com uma pergunta clara por experimento.
2. **O critério é a capacidade:** o que as pessoas passaram a conseguir fazer, entender ou fazer juntas que não conseguiam antes, e **para quem** isso vale.
3. **Registrar tudo, inclusive o que não deu certo.** Um experimento abandonado e bem registrado vale tanto quanto um bem-sucedido.
4. **Qualquer espaço pode propor.** Biblioteca, escola, associação, grupo de moradores.
5. **O conselho cuida dos riscos, não do mérito.** Ele aprova experimentos olhando dados pessoais, segurança e a licença do acervo; não decide de antemão se a ideia é boa.
6. **Espaço para o que não cabe nas métricas.** Parte dos ciclos fica reservada a propostas livres, que talvez nunca se encaixem num indicador.

## Cardápio de experimentos

| # | Experimento | O que muda | Pergunta que testa | Como montar |
| --- | --- | --- | --- | --- |
| 1 | **Modo biblioteca** | A interface deixa de simular conversa: o assistente mostra primeiro os trechos e as páginas do acervo, e só depois, se pedido, um resumo curto | Mostrar as fontes antes aumenta a leitura e reduz a delegação? | Assistente com o prompt [`modo-biblioteca.md`](../../prompts/pt/modo-biblioteca.md) |
| 2 | **Só perguntas** | O assistente nunca responde diretamente; só faz perguntas e indica o que ler | Um grupo aprende mais quando é obrigado a construir a resposta? | Prompt [`so-perguntas.md`](../../prompts/pt/so-perguntas.md) |
| 3 | **Acervo primeiro** | A porta de entrada é a wiki; o assistente só é acessado a partir de uma página ("pergunte sobre esta página") | O acervo passa a ser lido e corrigido mais quando é o centro? | Link em cada página da wiki para o assistente, com a pergunta pré-preenchida (o Open WebUI aceita o parâmetro `?q=` na URL; confira na sua versão) |
| 4 | **Leitura lado a lado** | Um grupo lê junto um documento difícil (edital, lei) e usa o assistente só para explicar termos e trechos | A IA ajuda mais como dicionário e comentador do que como resumidor? | Leitor de Documentos + oficina presencial ou online |
| 5 | **Do individual ao coletivo** | A ficha de solução ganha a pergunta "isso afeta outras pessoas?"; se sim, o caso é encaminhado a uma associação, conselho ou ouvidoria | Soluções individuais viram pauta comum? | Campo novo na [ficha de solução](../../wiki-modelos/ficha-de-solucao.md) |
| 6 | **Interrogar a história** | Uma turma de escola escreve páginas de memória local e usa o assistente para confrontar versões oficiais e relatos de moradores | Os estudantes passam a ver a história a partir do próprio lugar? | Parceria com escola; camada `memoria/` |
| 7 | **Na nossa língua** | Glossário local, expressões e variantes da fala da região entram no acervo e nos prompts; em parceria, uma língua indígena ou de imigração da região | A ferramenta funciona para quem fala diferente da norma? | Só com a comunidade falante liderando e decidindo |
| 8 | **Um modelo nosso** | Um modelo aberto pequeno é ajustado (*fine-tuning*) com o acervo curado, numa GPU de universidade, e comparado ao modelo geral com busca | Um modelo formado pelo acervo local responde melhor, ou de forma diferente? | Exige autorização do conselho e consentimento dos autores (novo campo no [termo](../../templates/pt/termo-consentimento-memoria-oral.md)); nunca uso comercial |
| 9 | **Sem IA** | A mesma oficina é feita sem o assistente, com o acervo impresso ou na tela | O que a IA acrescenta de fato? O que ela tira? | Grupo de comparação; mesma questão, mesmos mediadores |
| 10 | **Proposta livre** | Qualquer arranjo que um grupo queira testar | — | Registro de experimento + aprovação de riscos |

## Como conduzir um ciclo

1. **Propor.** Preencha o [registro de experimento](../../templates/pt/registro-de-experimento.md) e publique em `experimentos/` na wiki.
2. **Aprovar os riscos.** O conselho confere dados pessoais, segurança e licença do acervo. Não julga o mérito.
3. **Montar.** No Open WebUI, cada variante é um assistente separado, com nome e versão: "Assistente do Acervo · modo biblioteca · v1". Nunca altere o assistente principal durante um experimento.
4. **Rodar de 4 a 6 semanas.** Com um grupo definido (uma turma, uma oficina, os usuários de uma biblioteca).
5. **Observar.** Com anotações dos mediadores, conversas com participantes e, só com consentimento explícito, trechos de uso anonimizados.
6. **Avaliar em roda.** Com quem participou, a partir das perguntas abaixo.
7. **Decidir e registrar.** Manter, modificar (novo ciclo) ou abandonar. O registro fica em `experimentos/` e, se servir a outras cidades, é compartilhado no GitHub do projeto (uma *issue* com o rótulo `experimento`).

## Perguntas para observar e avaliar

Essas perguntas não são uma lista de itens a cumprir; servem para abrir a conversa na roda.

- O que as pessoas passaram a conseguir fazer, entender ou fazer juntas que não conseguiam antes?
- Para quem funcionou? Para quem não funcionou, e por quê?
- O uso pareceu **cuidado** ou **vigilância**? **Aprendizado** ou **atalho**?
- As pessoas ficaram mais capazes de agir por conta própria, ou mais dependentes da ferramenta?
- O que surpreendeu?
- Apareceu algum valor ou preocupação que não estava previsto quando o experimento começou?
- O que outro espaço precisaria saber para tentar o mesmo?

## Uma rede, não um modelo

O repositório é um ponto de partida. Cada cidade pode criar suas variantes, e o valor da rede está em compartilhar os registros: o que foi tentado, o que as pessoas passaram a conseguir fazer, o que foi abandonado. Com o tempo, o conjunto de registros vale mais do que qualquer configuração padrão.
