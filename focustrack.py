# -*- coding: utf-8 -*-
"""
FOCUSTRACK - RASTREADOR DE SESSOES DE ESTUDO GAMIFICADO

Projeto pessoal, reconstruindo os conceitos do desafio SoulPass (FIAP)
em um tema proprio, escrito a mao para fins de aprendizado e portfolio.

Este programa implementa o CRUD (Criar, Ler, Atualizar, Deletar) da entidade
TB_SESSAO_ESTUDO, entidade associativa entre aluno e disciplina: registra
cada sessao de estudo realizada, o metodo usado (leitura, exercicio,
videoaula, resumo), o status da sessao e os pontos de XP conquistados.

Estrutura de dados: lista de dicionarios (colecao), em que cada dicionario
corresponde a um registro.
Persistencia: arquivo JSON local.
"""

# A partir daqui e com voce.
# Proximo passo: imports (json, os, datetime) + constantes de configuracao
# (nome do arquivo de dados, formato de data, numero maximo de tentativas)
# + os dois catalogos ALUNOS e DISCIPLINAS.
import json
import os
from datetime import datetime

ARQUIVO_DADOS = "sessoes_estudos.json"
FORMATO_DATA = '%d/%m/%Y'
MAX_TENTATIVAS = 3

METODOS_ESTUDOS= ("LEITURA","EXERCICIO","VIDEO_AULA","RESUMO")
STATUS_SESSAO = ("PENDENTE","CONCLUIDA","REVISAO")

class OperacaoCancelada(Exception):
    pass

ALUNOS = [
    {"id_aluno": 1, "nome":"Rodrigo", "email":"rodrigo@email.com", "ativo":"S"},
    {"id_aluno": 2, "nome":"Pedro", "email":"pedro@email.com", "ativo":"S"},
    {"id_aluno": 3, "nome":"Ana", "email":"ana@email.com", "ativo":"N"},
    {"id_aluno": 4, "nome":"Marcos", "email":"marcos@email.com", "ativo":"N"}
]

DISCIPLINAS = [
    {"id_disciplina": 1, "nome_disciplina": "Python", "carga_horaria_meta": 120, "ativa": "S"},
    {"id_disciplina": 2, "nome_disciplina": "Java", "carga_horaria_meta": 90, "ativa": "N"},
    {"id_disciplina": 3, "nome_disciplina": "IA", "carga_horaria_meta": 100, "ativa": "S"},
    {"id_disciplina": 4, "nome_disciplina": "Front", "carga_horaria_meta": 60, "ativa": "N"}
]

def exibir_cabecalho(titulo):
    print("=" * 50)
    print(titulo.center(50))
    print("=" * 50)
    return None

def listar_catalogo(colecao,chave_id,chave_descricao, titulo):
    exibir_cabecalho(titulo)
    for item in colecao:
        print(item[chave_id], "-", item[chave_descricao])
    return len(colecao)    


def carregar_dados(arquivo_dados):
    if not os.path.exists(arquivo_dados):
        return []
    try:
        with open(arquivo_dados, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except json.JSONDecodeError as erro:
        print(f"O arquivo {arquivo_dados} esta corrompido: {erro}")
        raise
    except OSError as erro:
        print(f"Nao foi possivel ler {arquivo_dados}: {erro}")
        raise
    else:
        return dados

def salvar_dados(dados, arquivo_dados):
    try:
        with open(arquivo_dados, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    except OSError as erro:
        print(f"Nao foi possivel salvar {arquivo_dados}: {erro}")
        raise
    else:
        print("Os dados foram salvos!")


def ler_inteiro(mensagem, minimo, maximo):
    for tentativa in range(MAX_TENTATIVAS):
        restantes = MAX_TENTATIVAS - tentativa - 1
        try:
            numero = int(input(mensagem))
        except ValueError:
            print(f"Digite um numero inteiro. Restam {restantes} tentativa(s).")
            continue
        if minimo <= numero <= maximo:
            return numero
        print(f"Valor fora da faixa ({minimo} a {maximo}). Restam {restantes} tentativa(s).")
    raise OperacaoCancelada("Tentativas esgotadas. Operacao cancelada.")
        
def ler_opcao(mensagem, opcoes):
    for tentativa in range(MAX_TENTATIVAS):
        restantes = MAX_TENTATIVAS - tentativa - 1
        opcao = input(mensagem).upper().strip()
        if opcao in opcoes:
            return opcao
        print(f"Opcao invalida. Opcoes: {', '.join(opcoes)}. Restam {restantes} tentativa(s).")
    raise OperacaoCancelada("Tentativas esgotadas. Operacao cancelada.")      
    
def ler_data(mensagem):
    for tentativa in range(MAX_TENTATIVAS):
        restantes = MAX_TENTATIVAS - tentativa - 1
        texto = input(mensagem).strip()
        try:
            datetime.strptime(texto, FORMATO_DATA)
        except ValueError:
            print(f'Data incorreta,use dd/mm/aaaa. Restam {restantes} tentativas')
            continue
        return texto
    raise OperacaoCancelada("Tentativas esgotadas. Operacao cancelada.")

def ler_texto(mensagem):
    for tentativa in range(MAX_TENTATIVAS):
        restantes = MAX_TENTATIVAS - tentativa - 1
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print(f"O texto nao pode ser vazio. {restantes} restantes")
    raise OperacaoCancelada("Tentativas esgotadas. Operacao cancelada.")  


    



        



