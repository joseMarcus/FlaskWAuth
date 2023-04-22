from flask import Flask, Blueprint
from flask_restful import Api
from database import db
from cors import cors
from flask_migrate import Migrate
from resources.Pessoa import PessoaResource, PessoasResource
from config import DevelopmentConfig, ProductionConfig, TestingConfig


app = Flask(__name__)



# Criado um objeto de configuração com base na variável de ambiente FLASK_ENV
if app.config['ENV'] == 'production':
    app.config.from_object(ProductionConfig())
elif app.config['ENV'] == 'testing':
    app.config.from_object(TestingConfig())
else:
    app.config.from_object(DevelopmentConfig())


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='/api')

db.init_app(app)
cors.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


api.add_resource(PessoaResource, '/pessoas')
api.add_resource(PessoasResource, '/pessoas/<pessoa_id>')


app.register_blueprint(api_bp)



if __name__ == '__main__':
    app.run()