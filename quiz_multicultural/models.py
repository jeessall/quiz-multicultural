from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pontuacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_jogador = db.Column(db.String(80), nullable=False)
    nivel = db.Column(db.String(10), nullable=False)
    pontos = db.Column(db.Integer, nullable=False)