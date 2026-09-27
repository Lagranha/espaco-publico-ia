# 1. Proposta

> O Espaço Público IA é um acervo vivo da cidade, online e gratuito, com um assistente de IA que responde a partir dele. O acervo cresce com o que os moradores resolvem, é protegido contra o uso para treinar IAs comerciais, e a inteligência artificial vem de infraestrutura pública suíça emprestada, não de big techs.

## A ideia

A biblioteca pública garantiu o acesso ao livro sem cobrar por página. O Espaço Público IA aplica a mesma lógica à inteligência artificial e ao conhecimento sobre a própria cidade. A inspiração é uma sugestão do pesquisador Evgeny Morozov: criar instituições intermediárias, como as bibliotecas, que ofereçam IA como infraestrutura pública, e não como serviço cobrado por uso.

Ele é a versão online do [Laboratório Público de IA](https://github.com/Lagranha/laboratorio-publico-ia), que roda num computador dentro de uma biblioteca. Aqui, qualquer pessoa cadastrada usa de casa, pelo celular ou pelo computador.

## Quatro ideias centrais

**1. Um acervo da cidade, em três camadas.** Documentos oficiais (leis, planos, cartilhas), memória local (entrevistas, histórias, estudos) e fichas de solução (como moradores resolveram problemas reais). O assistente sempre diz de qual camada vem cada informação, para não confundir relato com documento oficial.

**2. Um acervo que cresce com o uso.** Quem resolve um problema pode escrever uma ficha de solução, que é revisada e entra no acervo. Quando o assistente não sabe responder, a pergunta vira uma lacuna, e a comunidade é convidada a preenchê-la.

**3. Um acervo protegido.** O conteúdo é de guarda comunitária: serve à comunidade e não pode ser usado para treinar modelos de IA, especialmente os comerciais. A proteção combina cadastro obrigatório, licença própria, bloqueio de robôs e frases-canário para detectar uso indevido.

**4. IA de infraestrutura pública.** As respostas vêm do **Apertus**, um modelo aberto criado por universidades públicas suíças (EPFL, ETH Zurique e o centro nacional de supercomputação suíço, CSCS), usado por meio do **Public AI Inference Utility**, um serviço sem fins lucrativos. O acervo fica no nosso servidor; só a pergunta e os trechos necessários viajam para gerar cada resposta.

## Para quem

Moradores que precisam entender um serviço público ou resolver um problema; conselheiros municipais, jornalistas locais, professores e estudantes; associações, cooperativas e pequenos negócios; mediadores de bibliotecas e escolas, que usam o Espaço em oficinas.

## O que isto não é

- Não é um chatbot genérico: o assistente responde a partir do acervo da cidade e diz quando não sabe.
- Não é independente de tudo: o serviço suíço usa parceiros de computação, entre eles a Amazon Web Services. A dependência de grandes empresas é **mínima e transparente**, não zero. Veja [a IA pública suíça](03-ia-publica-suica.md).
- Não substitui a presença: funciona melhor ligado a espaços físicos (bibliotecas, escolas, associações) com mediadores.
