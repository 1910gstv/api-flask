from ..models import formacao_model
from api import db
from .professor_service import listar_professor_id

def cadastrar_formacao(formacao):
    formacao_db = formacao_model.Formacao(nome=formacao.nome, descricao=formacao.descricao)
    for i in formacao.professores:
        professor = listar_professor_id(i)
        formacao_db.professores.append(professor)
    db.session.add(formacao_db)
    db.session.commit()
    return formacao_db

def listar_formacoes():
    formacoes = formacao_model.Formacao.query.all()
    return formacoes

def listar_formacao_id(id):
    formacao = formacao_model.Formacao.query.filter_by(id=id).first()
    return formacao

def atualizar_formacao(formacao_anterior, formacao_novo):
    formacao_anterior.nome = formacao_novo.nome
    formacao_anterior.descricao = formacao_novo.descricao
    for i in formacao_novo.professores:
        professor = listar_professor_id(i)
        formacao_anterior.professores.append(professor)
    db.session.commit()

def remover_formacao(formacao):
    db.session.delete(formacao)
    db.session.commit()