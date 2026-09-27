# 9. Piloto e custos

> Um piloto de 12 semanas numa cidade, com uma instituição-âncora, 50 a 100 documentos iniciais e 100 a 300 usuários convidados. Custo mensal estimado entre R$ 200 e R$ 600, mais as bolsas.

## Etapas

1. **Semanas 1–2: base.** Instituição-âncora e conselho; servidor no ar; conta no Public AI e carta pedindo um acordo institucional.
2. **Semanas 3–4: acervo inicial.** 50 a 100 páginas em `oficial/` e `memoria/`; 10 fichas de solução escritas em oficinas presenciais; canários inseridos.
3. **Semanas 5–6: teste fechado.** 20 pessoas (mediadores, conselheiros, bibliotecários) usam e fazem "Confira a fonte"; teste Apertus 8B × 70B com `tools/avaliar_modelos.py`; ajustes nos prompts.
4. **Semanas 7–12: abertura por convite.** Cadastro via instituições parceiras (bibliotecas, escolas, associações); atividades em casa; duas rodas online; primeiras lacunas preenchidas.
5. **Semana 12: avaliação.** Relatório público e decisão do conselho.

## Custos aproximados (Brasil, setembro de 2026)

| Item | Mensal | Observação |
| --- | --- | --- |
| Servidor (4–8 vCPU, 16 GB, sem GPU) | R$ 0 a 400 | Zero se cedido por universidade ou prefeitura; senão, provedor brasileiro (cotar) |
| IA (Public AI, Apertus 70B) | ≈ US$ 3 a 32 | De 1 mil a 10 mil perguntas por mês; ver [cálculo](03-ia-publica-suica.md#quanto-custa-por-pergunta) |
| Domínio e e-mail | ≈ R$ 20 | |
| Bolsas: técnico (10 h/semana) e curadoria (10 h/semana) | R$ 2 a 3 mil | O custo principal é gente |

O custo da IA é pequeno perto do resto: a infraestrutura pública emprestada torna o serviço viável para cidades pequenas.

## O que medir

- **Qualidade:** percentual de respostas com fonte correta (atividade "Confira a fonte").
- **Crescimento do acervo:** fichas aprovadas, lacunas preenchidas, documentos incluídos.
- **Uso qualificado:** perguntas por pessoa, problemas resolvidos relatados, instituições parceiras usando em oficinas.
- **Proteção:** tentativas de robôs bloqueadas (logs do Caddy), canários verificados.
- **Custo por pergunta**, conferido no painel do Public AI.

Não medir tempo de tela nem mensagens por dia como sucesso.

## Fase 2

- **Login único** para wiki e assistente (OpenID Connect, com Keycloak ou Authentik).
- Botão "transformar esta conversa numa ficha", que preenche o modelo com o que foi resolvido.
- Rede de cidades compartilhando o mesmo servidor, cada uma com seu acervo e seu conselho.
- Migração da inferência para GPU de universidade brasileira rodando o Apertus: dependência zero de big techs.
- Integração com um leitor automático do Diário Oficial (projeto irmão "Diário Oficial em Linguagem Simples") como fonte da camada oficial.
