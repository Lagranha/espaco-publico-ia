# Modelos para a wiki · Wiki templates

## Estrutura de páginas (o caminho define a camada)

| Caminho na wiki | Camada | Vai para o assistente? | Quem escreve |
| --- | --- | --- | --- |
| `inicio` | Página de boas-vindas | Não | Curadores |
| `oficial/...` | Documentos oficiais | Sim | Curadores |
| `memoria/...` | Memória local | Sim, quando publicada | Curadores (com consentimento) |
| `fichas/rascunhos/...` | Fichas em revisão | Não | Contribuidores |
| `fichas/...` | Fichas de solução aprovadas | Sim | Curadores movem do rascunho |
| `lacunas` | Lacunas públicas (perguntas sem resposta, revisadas) | Não | Curadores |
| `curadoria/...` | Área interna (lacunas brutas, canários, atas) | Não | Só curadores leem |
| `atividades/...` | Trilhas e atividades para fazer em casa | Não | Mediadores |
| `experimentos/...` | Registros de experimentos (proposta e resultados) | Não | Quem propõe; mediadores |

O sincronizador (`tools/sincronizar_acervo.py`) só envia ao assistente as páginas **publicadas** em `oficial/`, `memoria/` e `fichas/` (exceto `fichas/rascunhos/`).

## Grupos e permissões no Wiki.js

Configure em *Administração → Grupos* (as regras de página usam "caminho começa com"):

| Grupo | Ler | Escrever |
| --- | --- | --- |
| Visitantes (Guests) | nada | nada |
| Leitores (padrão de novos cadastros) | tudo, exceto `curadoria/` | nada |
| Contribuidores | tudo, exceto `curadoria/` | `fichas/rascunhos/` e comentários |
| Curadores | tudo | tudo |

## Arquivos

- [`ficha-de-solucao.md`](ficha-de-solucao.md): modelo de ficha, para criar em `fichas/rascunhos/`.
- [`inicio.md`](inicio.md): texto sugerido para a página inicial.
- [`lacunas.md`](lacunas.md): página pública de lacunas.
