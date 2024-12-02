from flask_restful import  Resource
from api import api
from ..schemas import professor_schema
from flask import request,make_response, jsonify
from ..entidades import professor
from ..services import professor_service

class ProfessorList(Resource):
    def get(self):
        formacoes = professor_service.listar_professores()
        fs = professor_schema.ProfessorSchema(many=True)
        return make_response(fs.jsonify(formacoes), 200)

    def post(self):
        fs = professor_schema.ProfessorSchema()
        validate = fs.validate(request.json)

        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json['nome']
            idade = request.json['idade']

            novo_professor = professor.Professor(nome=nome,idade=idade)
            resultado = professor_service.cadastrar_professor(novo_professor)
            x = fs.jsonify(resultado)

            return make_response(x, 201)

class ProfessorDetail(Resource):
    def get(self, id):
        professor = professor_service.listar_professor_id(id)
        if professor is None:
            return make_response(jsonify('Formação Não Encontrada'), 404)
        fs = professor_schema.ProfessorSchema()
        return make_response(fs.jsonify(professor), 200)

    def put(self,id):
        professor_db = professor_service.listar_professor_id(id)
        if professor_db is None:
            return make_response(jsonify('Formação Não Encontrada'), 404)
        fs = professor_schema.ProfessorSchema()
        validate = fs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json['nome']
            idade = request.json['idade']

            novo_professor = professor.Professor(nome=nome, idade=idade)
            professor_service.atualizar_professor(professor_db, novo_professor)
            professor_atualizado = professor_service.listar_professor_id(id)
            return make_response(fs.jsonify(professor_atualizado),200)

    def delete(self, id):
        professor_db = professor_service.listar_professor_id(id)
        if professor_db is None:
            return make_response(jsonify('Formação Não Encontrada'), 404)
        professor_service.remover_professor(professor_db)
        return make_response(jsonify('Formação excluída com sucesso!'), 204)

api.add_resource(ProfessorList, '/professor')
api.add_resource(ProfessorDetail,'/professor/<int:id>')
