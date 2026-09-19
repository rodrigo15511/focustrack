# FocusTrack - Notas do projeto

Ultima atualizacao: 19/09/2026

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
- **Validacao de entrada com retentativas** (passo 1 do roteiro concluido). As quatro funcoes seguem o mesmo padrao: `for` sobre `MAX_TENTATIVAS`, `restantes`, uma checagem, `return` do valor bom e, ao fim do laco, aviso + `return None`:
  - `ler_inteiro(mensagem, minimo, maximo)` - `int()` com `try/except ValueError` + checagem de faixa
  - `ler_opcao(mensagem, opcoes)` - `.strip().upper()` + `in`; mostra as opcoes validas no erro
  - `ler_data(mensagem)` - `datetime.strptime(texto, FORMATO_DATA)` com `try/except ValueError`; devolve o **texto** (JSON nao grava `datetime`)
  - `ler_texto(mensagem)` - recusa texto vazio ou so com espacos

Tudo testado rodando de verdade (entrada valida, invalida, e tentativas esgotadas).

## Pendencias conhecidas

- `carregar_dados` e `salvar_dados` ainda **sem try/except** (arquivo corrompido, falha de gravacao). Vai junto com o passo 2 (tratamento de excecoes).
- `listar_catalogo` ainda nao marca itens inativos (campos diferentes: `ativo` em ALUNOS, `ativa` em DISCIPLINAS).
- `ler_data` aceita `5/9/2026` (sem zero a esquerda) e devolve do jeito digitado. Para padronizar, guardar o resultado do `strptime` e devolver `.strftime(FORMATO_DATA)`.
- Mensagens de erro de `ler_data`/`ler_texto` usam `tentativas`/`restantes` em vez de `tentativa(s)` como as outras; padronizar se der vontade.
- Estilo: `return[]` na linha 62 sem espaco; `METODOS_ESTUDOS=` sem espaco antes do `=`; comentario "A partir daqui e com voce" no topo do arquivo esta desatualizado; linhas em branco e espacos sobrando no fim do arquivo.

## Proximo passo

**Passo 2: tratamento de excecoes** (`try/except/else/finally` + excecao customizada `OperacaoCancelada`). Conexao com o que ja existe: hoje as quatro funcoes de leitura devolvem `None` quando as tentativas acabam; o passo 2 troca isso por levantar `OperacaoCancelada`, e quem chama nao precisa checar `None` toda vez.

Ordem do roteiro do SoulPass:

1. ~~Validacao de entrada com retentativas~~ (feito)
2. Tratamento de excecoes (try/except/else/finally + excecao customizada tipo `OperacaoCancelada`)
3. Regras de negocio (simulando FK/CHECK)
4. CRUD completo de `TB_SESSAO_ESTUDO`
5. Menu principal em loop + submenus

## Ideia para depois do CRUD (evolucao do projeto)

Decisao: evoluir no **mesmo repositorio**, em fases, em vez de comecar outro projeto. React nao fala direto com o banco, entao o caminho e `React -> API -> banco`.

1. Terminar o CLI (roteiro acima)
2. Trocar JSON por SQLite (`sqlite3`, ja vem no Python), mantendo o mesmo CLI: aprender SQL, FK, CHECK, JOIN
3. API em Python (FastAPI, com pagina de testes em `/docs`): rotas de CRUD (`GET/POST/PUT/DELETE /sessoes`), validacao e regras de negocio
4. Front-end em React consumindo a API (antes disso, base de JavaScript: funcoes, arrays, `fetch`, async/await)
5. Opcional: migrar para PostgreSQL

Cuidado ja no CLI: manter **regras de negocio em funcoes sem `input()`/`print()`** (recebem valores e devolvem resultado ou levantam excecao), para reaproveitar na API. Separar "pedir o dado" de "checar se o dado e valido". Sugestao: marcar a versao do CLI com uma tag (`v1-cli`) antes de mexer.

## Licoes ate agora

- Em f-string, so o que esta dentro de `{}` e codigo; o resto e texto literal. Metodo se chama direto: `titulo.center(50)`.
- `item[chave_id]` (variavel, sem aspas) vs `item["chave_id"]` (chave literal).
- `return` encerra a funcao na hora (guard clause); `print` mostra, `return` devolve valor reutilizavel.
- Parametros de funcao em `snake_case` minusculo; CAIXA_ALTA e para constantes.
- Colecao de sessoes e uma **lista** (`[]`), nao dicionario (`{}`).
- **Tentativas vs faixa valida sao coisas diferentes**: `MAX_TENTATIVAS` controla quantas chances (constante + `for`); `minimo`/`maximo` sao a faixa do valor (parametros). Nao misturar.
- **Parametro e o que a funcao precisa saber antes de comecar.** O que ela descobre ao rodar (o que o usuario digita) e variavel interna, nao parametro.
- `restantes = MAX_TENTATIVAS - tentativa - 1`: `range` comeca em 0 e a tentativa atual ja esta sendo gasta.
- Comparar: `==` pergunta "e igual a"; `in` pergunta "esta dentro de". Um texto nunca e `==` a uma tupla, mas pode estar `in` ela.
- `input()` nunca devolve `None`: sem digitar nada devolve `""` (falso numa condicao, entao `if texto:` serve).
- `print` para avisar o usuario, `return` para entregar o valor. Aviso nao vai em `return`.
- O `return None` de "tentativas esgotadas" fica **fora** do `for`, na coluna dele; dentro, cancelaria na primeira falha.
- `try/except` fica so em volta da linha que pode falhar, e captura o erro especifico (`except ValueError:`), nunca `except:` puro.
- Nao usar nomes que ja existem no Python (`max`, `id`) para variaveis.
- Metodo de teste: `printf 'entrada1\nentrada2\n' | python -c "from focustrack import funcao; print(funcao(...))"`.
