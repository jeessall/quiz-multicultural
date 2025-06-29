# create_tables.py
from app import app, db

# Coloca o script no contexto da aplicação Flask
with app.app_context():
    print("Criando tabelas no banco de dados de produção...")
    db.create_all()
    print("Tabelas criadas com sucesso!")