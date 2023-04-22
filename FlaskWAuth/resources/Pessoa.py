from flask_restful import Resource, reqparse, marshal_with, marshal
from database import db
from flask_httpauth import HTTPBasicAuth

from model.pessoa import Pessoa, pessoa_fields
from model.mensagem import Mensagem, mensagem_fields
from logger import log

auth = HTTPBasicAuth()

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome')
parser.add_argument('sexo', type=str, help='Problema na conversão do sexo')
parser.add_argument('idade', type=int, help='Problema na conversão da idade')

@auth.verify_password
def verify_password(username, password):
    # Aqui você deve verificar se o nome de usuário e a senha fornecidos são válidos
    if username == 'user' and password == 'password':
        return True
    return False

class PessoaResource(Resource):
    @auth.login_required
    @marshal_with(pessoa_fields)
    def get(self):
        pessoas = Pessoa.query.filter_by(excluido=False).all()
        return (pessoas, 201)
        
    @auth.login_required
    @marshal_with(pessoa_fields)  
    def post(self):
        args = parser.parse_args()
        nome = args['nome']
        sexo = args['sexo']
        idade = args['idade']
        
        pessoa = Pessoa(nome, sexo, idade)

        db.session.add(pessoa)
        db.session.commit()

        return pessoa, 201
    
class PessoasResource(Resource):
    @auth.login_required

    def get(self, pessoa_id):
        log.info("Identificador de pessoa: " + pessoa_id)
        pessoa = Pessoa.query.filter_by(id=pessoa_id, excluido=False).first()

        if (pessoa is not None):
            return marshal(pessoa, pessoa_fields), 201
        else:
            mensagem = Mensagem('Pessoa não encontrada', 1)
            return marshal(mensagem, mensagem_fields), 404
    @auth.login_required

    @marshal_with(pessoa_fields)
    def put(self, pessoa_id):

        args = parser.parse_args()
        nome = args['nome']
        sexo = args['sexo']
        idade = args['idade']

        pessoa = Pessoa.query.filter_by(id=pessoa_id, excluido=False).first()

        if pessoa is not None:
            pessoa.nome = nome
            pessoa.sexo = sexo
            pessoa.idade = idade

            db.session.add(pessoa)
            db.session.commit()

            return marshal(pessoa, pessoa_fields), 201

        else:
            mensagem = Mensagem('Pessoa não encontrada', 1)
            return marshal(mensagem, mensagem_fields), 404
        
        return pessoa
    @auth.login_required

    def delete(self, pessoa_id):
        pessoa = Pessoa.query.filter_by(id=pessoa_id, excluido=False).first()

        if pessoa is not None:
            pessoa.excluido = True #para delete físico troca isso aqui por "db.session.delete(pessoa)"
            db.session.commit()

            mensagem = Mensagem('Pessoa excluída com sucesso', 0)
            return marshal(mensagem, mensagem_fields), 200

        else:
            mensagem = Mensagem('Pessoa não encontrada', 1)
            return marshal(mensagem, mensagem_fields), 404
