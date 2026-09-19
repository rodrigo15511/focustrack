# FocusTrack - Notas do projeto

Ultima atualizacao: 18/09/2026

## O que e

Rastreador de sessoes de estudo gamificado (`focustrack.py`). Reconstrucao, escrita a mao, dos conceitos do desafio FIAP SoulPass (`soulpassa.py`) em um tema proprio, para aprendizado e portfolio.

Entidade principal: `TB_SESSAO_ESTUDO` (aluno + disciplina + metodo + status + XP).
Estrutura de dados: lista de dicionarios. Persistencia: arquivo JSON (`sessoes_estudos.json`).

Mapeamento em relacao ao SoulPass:

| SoulPass | FocusTrack |
|---|---|
| `USUARIOS` | `ALUNOS` |
| `MISSOES` | `DISCIPLINAS` |
| `TB_ACAO_REALIZADA` | `TB_SESSAO_ESTUDO` |
| `METODOS_VALIDACAO` | `METODOS_ESTUDOS` |
| `STATUS_APROVACAO` | `STATUS_SESSAO` |
| pontos por missao | XP por sessao concluida |

## Ja pronto

- Imports (`json`, `os`, `datetime`) e constantes: `ARQUIVO_DADOS`, `FORMATO_DATA`, `MAX_TENTATIVAS`
- Dominios fixos: `METODOS_ESTUDOS`, `STATUS_SESSAO`
- Catalogos `ALUNOS` e `DISCIPLINAS` (4 registros cada, com ativos e inativos)
- `exibir_cabecalho(titulo)` - cabecalho padronizado, largura 50
- `listar_catalogo(colecao, chave_id, chave_descricao, titulo)` - listagem generica, retorna `len(colecao)`
- `carregar_dados(arquivo_dados)` - le o JSON; devolve `[]` se o arquivo nao existe
- `salvar_dados(dados, arquivo_dados)` - grava a lista no JSON (`ensure_ascii=False`, `indent=4`)

Tudo testado rodando de verdade.

## Pendencias conhecidas

- `carregar_dados` e `salvar_dados` ainda **sem try/except** (arquivo corrompido, falha de gravacao). Combinado adicionar junto da validacao de entrada.
- `listar_catalogo` ainda nao marca itens inativos (campos diferentes: `ativo` em ALUNOS, `ativa` em DISCIPLINAS).
- Estilo: `return[]` na linha 62 sem espaco; comentario "A partir daqui e com voce" no topo do arquivo esta desatualizado.

## Proximo passo

**Validacao de entrada com retentativas**, usando `MAX_TENTATIVAS`. Depois, na ordem do roteiro do SoulPass:

1. Validacao de entrada com retentativas
2. Tratamento de excecoes (try/except/else/finally + excecao customizada tipo `OperacaoCancelada`)
3. Regras de negocio (simulando FK/CHECK)
4. CRUD completo de `TB_SESSAO_ESTUDO`
5. Menu principal em loop + submenus

## Licoes ate agora

- Em f-string, so o que esta dentro de `{}` e codigo; o resto e texto literal. Metodo se chama direto: `titulo.center(50)`.
- `item[chave_id]` (variavel, sem aspas) vs `item["chave_id"]` (chave literal).
- `return` encerra a funcao na hora (guard clause); `print` mostra, `return` devolve valor reutilizavel.
- Parametros de funcao em `snake_case` minusculo; CAIXA_ALTA e para constantes.
- Colecao de sessoes e uma **lista** (`[]`), nao dicionario (`{}`).
