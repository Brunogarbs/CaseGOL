from flask import Flask, render_template, request, redirect,url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import db
from models import Usuario, DadosEstatisticos
from io import BytesIO
import base64
from datetime import datetime
import plotly.express as px
import plotly.io as pio
import pandas as pd
from sqlalchemy import String, case, func
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
lm = LoginManager(app)
app.secret_key = 'ceci'
lm.login_view = 'Login'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)


@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id=id).first() 
    return  usuario


@app.route('/', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']

        # Buscar o usuário pelo nome no banco de dados
        login = db.session.query(Usuario).filter_by(usuario=usuario).first()

        # Verificar se o usuário existe e se a senha está correta
        if not login or not check_password_hash(login.senha, senha):
            return render_template('Login.html', erro='Nome ou senha incorreta.')

        login_user(login)
        return redirect(url_for('Home'))

    return render_template('Login.html')

@app.route('/Home',methods = ['GET', 'POST'])
@login_required
def Home():
    mercados = db.session.query(DadosEstatisticos.mercado).distinct().all()
    mercados = [mercado[0] for mercado in mercados]

    anos = db.session.query(DadosEstatisticos.ano).distinct().order_by(DadosEstatisticos.ano.asc()).all()
    anos = [ano[0] for ano in anos]

    meses = db.session.query(DadosEstatisticos.mes).distinct().order_by(DadosEstatisticos.mes.asc()).all()
    meses = [mes[0] for mes in meses]

    filtro = []

    if request.method == 'POST':
        mercado_selecionado = request.form.get('mercado')
        ano_selecionado = request.form.get('ano')
        mes_selecionado = request.form.get('mes')

        query = DadosEstatisticos.query

        if mercado_selecionado:
            query = query.filter(DadosEstatisticos.mercado == mercado_selecionado)

        if ano_selecionado:
            query = query.filter(DadosEstatisticos.ano == int(ano_selecionado))
        
        if mes_selecionado:
            query = query.filter(DadosEstatisticos.mes == int(mes_selecionado))
        
        filtro = query.all()

    return render_template('Home.html', mercados = mercados, anos = anos, meses = meses, dados = filtro)

@app.route('/get_anos_e_meses', methods=['GET'])
def get_anos_e_meses():
    mercado = request.args.get('mercado')

    # Obtenha os anos e meses para o mercado selecionado
    anos = db.session.query(DadosEstatisticos.ano).filter(DadosEstatisticos.mercado == mercado).distinct().order_by(DadosEstatisticos.ano.asc()).all()
    anos = [ano[0] for ano in anos]

    meses = db.session.query(DadosEstatisticos.mes).filter(DadosEstatisticos.mercado == mercado).distinct().order_by(DadosEstatisticos.mes.asc()).all()
    meses = [mes[0] for mes in meses]

    return jsonify({'anos': anos, 'meses': meses})

@app.route('/Grafico', methods = ['GET','POST'])
@login_required
def Grafico():
    mercados = db.session.query(DadosEstatisticos.mercado).distinct().all()
    mercados = [mercado[0] for mercado in mercados]

    filtro = []

    if request.method == 'POST':
        mercado_selecionado = request.form.get('mercado')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')

        query = DadosEstatisticos.query

        if mercado_selecionado:
            query = query.filter(DadosEstatisticos.mercado == mercado_selecionado)
        
        if data_inicio and data_fim:
            query = query.filter(
                func.concat(
                    DadosEstatisticos.ano, '-', 
                    case(
                        (DadosEstatisticos.mes < 10, '0' + func.cast(DadosEstatisticos.mes, String)),
                        else_=func.cast(DadosEstatisticos.mes, String)
                    )
                ) >= data_inicio,
                
                func.concat(
                    DadosEstatisticos.ano, '-', 
                    case(
                        (DadosEstatisticos.mes < 10, '0' + func.cast(DadosEstatisticos.mes, String)),
                        else_=func.cast(DadosEstatisticos.mes, String)
                    )
                ) <= data_fim
            )
        filtro = query.all()

        if filtro:
            df = pd.DataFrame([{
                'Data': datetime(int(dado.ano), int(dado.mes), 1),
                'RPK': dado.rpk
            } for dado in filtro])

            fig = px.line(df, x='Data', y='RPK', title='RPK por Data', labels={'Data': 'Data', 'RPK': 'Revenue per Kilometer'})

            img_bytes = fig.to_image(format="png")
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')

            return render_template('Grafico.html', mercados=mercados, dados=filtro, img_base64=img_base64)

    return render_template('Grafico.html', mercados=mercados, dados=filtro)

@app.route('/get_datas_disponiveis', methods=['POST'])
def get_datas_disponiveis():
    mercado = request.json.get('mercado')
    
    if mercado:
        datas_disponiveis = db.session.query(DadosEstatisticos.ano, DadosEstatisticos.mes)\
            .filter(DadosEstatisticos.mercado == mercado)\
            .order_by(DadosEstatisticos.ano, DadosEstatisticos.mes)\
            .all()

        # Converte as datas disponíveis para o formato 'YYYY-MM'
        datas_formatadas = [f"{ano}-{str(mes).zfill(2)}" for ano, mes in datas_disponiveis]
        return jsonify(datas_formatadas)

    return jsonify([])


@app.route('/Cadastro', methods=['GET', 'POST'])
def Cadastro():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']

        # Verificar se o usuário já existe no banco de dados
        usuario_existente = db.session.query(Usuario).filter_by(usuario=usuario).first()
        if usuario_existente:
            return render_template('Cadastro.html', erro='Usuário já cadastrado.')

        # Fazer o hash da senha antes de salvar no banco
        senha_hashed = generate_password_hash(senha)

        # Criar novo usuário e salvar no banco de dados
        cadastro = Usuario(usuario=usuario, senha=senha_hashed)
        db.session.add(cadastro)
        db.session.commit()

        login_user(cadastro)
        return redirect(url_for('Login'))
    
    return render_template('Cadastro.html')

@app.route('/Logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('Login')) 
 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

