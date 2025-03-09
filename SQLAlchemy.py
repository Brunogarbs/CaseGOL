from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Definindo o modelo da tabela
class DadosEstatisticos(db.Model):
    __tablename__ = 'Dados_Estatisticos_GLO'

    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    mercado = db.Column(db.String(15), nullable=False)
    rpk = db.Column(db.Integer, nullable=False)

# Criar a tabela no banco de dados
with app.app_context():
    db.create_all()

# Carregar dados do Excel
def importar_dados_do_excel(arquivo_excel):
    df = pd.read_excel(arquivo_excel)  # Lê o arquivo Excel
    with app.app_context():  # Garantir que o contexto da aplicação esteja ativo
        for _, row in df.iterrows():
            # Verificar se os dados são válidos (não são NaN e estão no formato correto)
            if pd.notna(row['ANO']) and pd.notna(row['MES']) and pd.notna(row['MERCADO']) and pd.notna(row['RPK']):
                dado = DadosEstatisticos(
                    ano=int(row['ANO']),
                    mes=int(row['MES']),
                    mercado=str(row['MERCADO']),
                    rpk=int(row['RPK'])
                )
                db.session.add(dado)
        db.session.commit()

# Exemplo de uso
if __name__ == '__main__':
    importar_dados_do_excel('C:/Users/Bruno/Bruno/Projetos/Case Entrevista/Auxiliar/Dados_Estatistico_GLO.xlsx')
