# ✈️ CaseGOL – Teste Técnico GOL Linhas Aéreas




Este projeto foi desenvolvido como parte de um teste técnico da GOL Linhas Aéreas, com o objetivo de construir uma aplicação web utilizando Python com Flask para visualização de dados por meio de gráficos interativos.

## 📊 Funcionalidades
Visualização gráfica de dados (gráficos de barras, linhas, entre outros)

Interface web simples e responsiva

Backend leve com Flask

Geração dinâmica de gráficos com base nos dados fornecidos

## 🛠 Tecnologias Utilizadas
Python 3.10+

Flask

Matplotlib / Plotly / Pandas (dependendo do gráfico gerado)

HTML5 / CSS3 / Jinja2

## 🚀 Como executar o projeto
1. Clone o repositório:

```bash
git clone https://github.com/Brunogarbs/CaseGOL.git
cd CaseGOL
```
2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Instale as dependências:

```bash
pip install -r requirements.txt
```
4. Execute a aplicação:
```bash
flask run
```
5. Acesse no navegador:
```bash
http://localhost:5000
```
## 📁 Estrutura do Projeto

CaseGOL/
│
├── app.py                 # Arquivo principal da aplicação Flask
├── templates/             # HTMLs com Jinja2
│   └── index.html
├── static/                # CSS/JS estáticos
├── charts/                # Geração de gráficos
├── data/                  # Arquivos de dados (CSV, JSON, etc.)
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo
## 📌 Considerações
Este projeto demonstrou a capacidade de:

Trabalhar com frameworks web leves como o Flask

Transformar dados em visualizações intuitivas

Estruturar uma aplicação Python com clareza e modularidade

## 📝 Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais informações.