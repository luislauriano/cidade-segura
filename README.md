## Descrição ℹ️
O Cidade Segura é uma plataforma de inteligência de dados desenvolvida para auxiliar as forças de segurança pública na otimização do patrulhamento e na prevenção de ocorrências. Utilizando um modelo de Machine Learning (XGBRegressor), a solução analisa dados históricos e em tempo real para prever a probabilidade de risco em diferentes regiões da cidade.

A ferramenta oferece um dashboard interativo onde os gestores de segurança podem:

Visualizar a previsão de risco para datas e horários futuros.

Analisar tendências e padrões históricos de ocorrências por zona, dia da semana e tipo de evento.

Tomar decisões baseadas em dados para alocar viaturas e pessoal de forma proativa, aumentando a eficiência e a segurança da população.

## Time 🏆
👨‍💻 Desenvolvedor
Luís Vinicius Lauriano de França
📧 E-mail: luislauriano@outlook.com.br
🌐 GitHub: luislauriano

## Documentação 📄

[Notebook de Treinamento e Engenharia de Variáveis:](https://github.com/luislauriano/cidade-segura/blob/main/Modelo_ML_Cidade_Segura.ipynb)

[Apresentação do Projeto (Pitch):]()

## Tecnologias ⚙️

### 🌐 Acessar a Aplicação Online
A plataforma está disponível para acesso e interação através do seguinte link:

🔗 [Acesse o Cidade Segura aqui!](https://cidade-segura.streamlit.app/)

### Como Executar o Projeto Localmente 🚀
Siga os passos abaixo para executar a solução localmente na sua máquina.

#### Clone o Repositório

* git clone [https://github.com/luislauriano/cidade-segura](https://github.com/luislauriano/cidade-segura) 
* cd cidade-segura

#### Crie um Ambiente Virtual (Recomendado)

* python -m venv venv
* source venv/bin/activate  # No Windows: venv\Scripts\activate

#### Instale as Dependências

  *   pip install -r requirements.txt

#### Execute a Aplicação Streamlit

* Certifique-se de que os arquivos model_cidade_segura.pkl.gz e Dados_tratados.csv estão na mesma pasta do seu app.py.

* streamlit run app.py

#### Acesse no Navegador

* Abra o seu navegador e acesse o endereço http://localhost:8501 para explorar a plataforma! 🔍
