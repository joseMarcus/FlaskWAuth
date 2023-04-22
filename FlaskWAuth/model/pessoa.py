from flask_restful import fields
from database import db




pessoa_fields = {
    'id':   fields.Integer,
    'nome':   fields.String,
    'sexo':   fields.String,
    'idade':   fields.Integer
      
}

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    sexo = db.Column(db.String, nullable=False )#unique=True, nullable=False(caso seja e-mail)
    idade = db.Column(db.Integer, nullable=False)
    excluido = db.Column(db.Boolean, default=False)

    

    def __init__(self, nome, sexo, idade):
        self.nome = nome
        self.sexo = sexo
        self.idade = idade
        self.excluido = False



    def __repr__(self):
        return f'<Pessoa {self.nome}, {self.sexo}, {self.idade}>'
    
    
   