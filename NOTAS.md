# FocusTrack - Notas do projeto

Ultima atualizacao: 22/09/2026 (passo 3 em andamento)

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
- `carregar_dados(arquivo_dados)` - le o JSON; devolve `[]` se o arquivo nao existe; `try/except/else` cobrindo `open`+`json.load`: `except json.JSONDecodeError` (arquivo corrompido) e `except OSError` (falha de leitura), cada um avisando com `print` e repetindo o erro (`raise` sozinho); `return dados` no `else`
- `salvar_dados(dados, arquivo_dados)` - grava a lista no JSON (`ensure_ascii=False`, `indent=4`); mesmo padrao: `try/except OSError/else`, avisa e repete o erro na falha, confirma ("Os dados foram salvos!") no `else`
- `OperacaoCancelada(Exception)` - excecao propria (corpo `pass`), definida depois das constantes. Significa "o usuario esgotou as tentativas e a operacao foi cancelada".
- `RegraNegocioVioloda(Exception)` - excecao propria (corpo `pass`) para regra de negocio violada (nome de classe com erro de digitacao - "Violoda" em vez de "Violada" -, mantido de proposito por enquanto, raise/except usam o mesmo nome em todo o arquivo).
- **Regras de negocio simulando FK/CHECK** (passo 3, inicio). Funcoes **sem `input()`/`print()`**: recebem valor, devolvem o registro ou levantam `RegraNegocioVioloda`.
  - `buscar_aluno(id_aluno)` / `buscar_disciplina(id_disciplina)` - procuram na lista (`for` + `if item["chave"] == valor: return item`), devolvem o dicionario ou `None` (FK: existe?)
  - `validar_aluno(id_aluno)` / `validar_disciplinas(id_disciplina)` - chamam o `buscar_*`; se `None`, `raise` (nao existe); se `aluno["ativo"] != "S"` / `disciplina["ativa"] != "S"`, `raise` (CHECK: inativo); senao devolvem o registro
- **Validacao de entrada com retentativas** (passo 1 do roteiro concluido). As quatro funcoes seguem o mesmo padrao: `for` sobre `MAX_TENTATIVAS`, `restantes`, uma checagem, `return` do valor bom e, ao fim do laco (fora do `for`), `raise OperacaoCancelada("Tentativas esgotadas. Operacao cancelada.")`. **Nenhuma devolve mais `None`.**
  - `ler_inteiro(mensagem, minimo, maximo)` - `int()` com `try/except ValueError` + checagem de faixa
  - `ler_opcao(mensagem, opcoes)` - `.strip().upper()` + `in`; mostra as opcoes validas no erro
  - `ler_data(mensagem)` - `datetime.strptime(texto, FORMATO_DATA)` com `try/except ValueError`; devolve o **texto** (JSON nao grava `datetime`)
  - `ler_texto(mensagem)` - recusa texto vazio ou so com espacos

Tudo testado rodando de verdade (entrada valida, invalida, tentativas esgotadas levantando `OperacaoCancelada`, arquivo corrompido, pasta inexistente).

**Passo 2 (tratamento de excecoes) concluido**, as quatro partes.

## Pendencias conhecidas

- A frase de `OperacaoCancelada` esta repetida nas quatro funcoes de leitura. Da para deixar o texto padrao dentro da propria classe (pede `__init__`, ainda nao visto).
- `salvar_dados` com `"w"` esvazia o arquivo antes de gravar; se o `json.dump` falhar no meio, o arquivo pode ficar incompleto. Melhoria futura: gravar em arquivo temporario e renomear.
- `json.dump` pode levantar `TypeError` se algum dado nao for serializavel (ex.: um `datetime` sem converter para texto); nao esta sendo tratado de proposito, deve aparecer como erro de codigo.
- `listar_catalogo` ainda nao marca itens inativos (campos diferentes: `ativo` em ALUNOS, `ativa` em DISCIPLINAS).
- `ler_data` aceita `5/9/2026` (sem zero a esquerda) e devolve do jeito digitado. Para padronizar, guardar o resultado do `strptime` e devolver `.strftime(FORMATO_DATA)`.
- Mensagens de erro de `ler_data`/`ler_texto` usam `tentativas`/`restantes` em vez de `tentativa(s)` como as outras; padronizar se der vontade.
- Estilo: `return[]` na linha 62 sem espaco; `METODOS_ESTUDOS=` sem espaco antes do `=`; comentario "A partir daqui e com voce" no topo do arquivo esta desatualizado; linhas em branco e espacos sobrando no fim do arquivo.

## Proximo passo

**Passo 3, continuacao:** `buscar_aluno`/`buscar_disciplina` e `validar_aluno`/`validar_disciplinas` prontas e testadas (aluno/disciplina existente ativo, existente inativo, inexistente). Falta decidir se entram mais regras aqui (ex.: XP so conta se status `CONCLUIDA`, minutos estudados deve ser positivo) antes de seguir pro passo 4 (CRUD) - em aberto.

Passo 2 (tratamento de excecoes) - **concluido**:

- ~~Parte 1: criar `OperacaoCancelada`~~
- ~~Parte 2: `raise` no lugar do `return None` em `ler_texto`~~
- ~~Parte 3: mesma troca em `ler_inteiro`, `ler_opcao`, `ler_data`~~
- ~~Parte 4: `try/except/else` em `carregar_dados` e `salvar_dados` (`json.JSONDecodeError` e `OSError`, aviso + `raise` sozinho, `else` para o caminho de sucesso)~~

Ordem do roteiro do SoulPass:

1. ~~Validacao de entrada com retentativas~~ (feito)
2. ~~Tratamento de excecoes (try/except/else + excecao customizada `OperacaoCancelada`)~~ (feito)
3. Regras de negocio (simulando FK/CHECK) - FK+CHECK de aluno/disciplina feitos, escopo aberto pra mais regras
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
- Metodo de teste: `printf 'entrada1\nentrada2\n' | python -c "from focustrack import funcao; print(funcao(...))"` (Git Bash), ou interativo (`python`, depois `from focustrack import ...`).
- **Excecoes:** `raise` dispara e encerra a funcao na hora; `except X` captura so o tipo `X`. A classe e so uma **etiqueta** (um nome): quem decide quando dispara e o `raise`, e o detalhe vai na mensagem entre parenteses (tem que ser string).
- **Classe e heranca:** `class A(B):` significa "A e um tipo de B" e A ganha tudo de B. `class OperacaoCancelada(Exception): pass` herda o poder de ser levantada e capturada. "Classe separada" = tipo a parte, nao arquivo a parte.
- **Quando criar excecao propria:** quando quem chama precisa reagir de forma diferente a essa situacao. Uma por situacao distinta, nao uma por erro pequeno.
- **Excecao nao passa despercebida como o `None`:** se ninguem captura, o programa cai com traceback claro.
- O `mensagem` de `ler_*` e a **pergunta** mostrada pelo `input`; a resposta se digita depois que ela aparece.
- No terminal: `>>>` = dentro do Python (so codigo Python); `$` / `PS C:\>` = shell (comandos). Nao misturar.
- **O Python nao recarrega modulo ja importado**: apos editar o arquivo, salvar (Ctrl+S) e sair/entrar de novo no `python` para testar a versao nova.
- **`with` dentro de `try` (nao o contrario):** `try` fica por fora, `with open(...)` fica dentro dele, recuado; assim o `try` cobre tambem o `open` (falha ao abrir), e nao so o que vem depois. Erro comum: `with ...:` seguido de `try:` na mesma coluna -> `IndentationError: expected an indented block after 'with' statement`.
- **`OSError`** cobre os erros de arquivo (`FileNotFoundError`, `PermissionError`, `IsADirectoryError` sao subclasses dele); um `except OSError` pega todos de uma vez.
- **`raise` sozinho** (sem nada depois), dentro de um `except`, repete o mesmo erro que acabou de ser capturado, sem adicionar uma linha nova ao traceback. Padrao usado: avisar com `print` (dizendo qual arquivo) e depois `raise`, para nao seguir em frente com dado incompleto/corrompido.
- **`else` do `try`** roda so quando nao houve erro; e o lugar certo do `return`/confirmacao de sucesso, separado do tratamento de erro.
- **FK/CHECK (conceito de banco) simulados a mao:** FK = a referencia (id) precisa existir na outra tabela/lista; CHECK = regra sobre o valor de um campo (ex.: status ativo). `buscar_*` resolve a FK (existe?); `validar_*` acrescenta o CHECK (existe E esta ativo?).
- **`is` vs `==`:** `is` pergunta "e o mesmo objeto na memoria?"; `==` pergunta "tem o mesmo valor?". Use `is None` (None e sempre o unico objeto do seu tipo). Para texto/numero, use `==`/`!=` - `is "N"` da SyntaxWarning do proprio Python ("Did you mean =="?) e pode falhar quando o valor vem de fora (JSON, banco), mesmo que hoje pareca funcionar por otimizacao interna do Python (strings curtas/literais).
- **Ordem importa em validacoes encadeadas:** so da pra checar `dado["campo"]` depois de confirmar que `dado` nao e `None`; senao quebra tentando indexar `None`.
- Preferir `!= "S"` a `== "N"` nessas checagens: se aparecer um valor inesperado (vazio, espaco, erro de digitacao), `!= "S"` ainda bloqueia (seguro); `== "N"` deixaria passar por engano.
