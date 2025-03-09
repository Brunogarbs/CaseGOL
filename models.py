from db import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key = True)
    usuario = db.Column(db.String(30), nullable = False,unique = True)
    senha = db.Column(db.String)

class DadosEstatisticos(db.Model):
    __tablename__ = 'Dados_Estatisticos_GLO'

    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    mercado = db.Column(db.String(15), nullable=False)
    rpk = db.Column(db.Integer, nullable=False)