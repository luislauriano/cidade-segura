import streamlit as st
import pandas as pd
import pickle
import gzip
import plotly.express as px
from datetime import datetime


with gzip.open('model_cidade_segura.pkl.gz', 'rb') as f:
    model = pickle.load(f)


lista_feriados = pd.to_datetime(['2025-01-01', '2025-04-21', '2025-09-07', '2025-10-12', '2025-11-15'])


@st.cache_data
def carregar_dados_historicos():
    """Carrega e prepara o dataset histórico, otimizado com cache."""
    df = pd.read_csv('Dados_tratados.csv')
    df['data'] = pd.to_datetime(df['data'])
    df = df.sort_values(by='data')
    return df

df_historico = carregar_dados_historicos()



def gerar_features_dinamicas(df_historico, zona_selecionada, tipo_ocorrencia_selecionado, data_previsao):
    """
    Calcula features complexas (baseadas em data e histórico) para uma única previsão futura.
    """
    data_previsao = pd.to_datetime(data_previsao)
    
   
    features = {
        'dia_da_semana': data_previsao.dayofweek,
        'final_de_semana': 1 if data_previsao.dayofweek >= 5 else 0,
        'mes': data_previsao.month,
        'semana_do_mes': (data_previsao.day - 1) // 7 + 1,
        'feriado': 1 if data_previsao.normalize() in lista_feriados else 0
    }

    
    hist_contexto = df_historico[
        (df_historico['zona'] == zona_selecionada) &
        (df_historico['tipo_ocorrencia'] == tipo_ocorrencia_selecionado) &
        (df_historico['data'] < data_previsao)
    ].copy()

    if not hist_contexto.empty:
        hist_contexto['media_3dias_calc'] = hist_contexto['risco_ocorrencia'].rolling(window=3, min_periods=1).mean()
        hist_contexto['media_7dias_calc'] = hist_contexto['risco_ocorrencia'].rolling(window=7, min_periods=1).mean()
        hist_contexto['media_7dias_anterior_calc'] = hist_contexto['risco_ocorrencia'].shift(1).rolling(window=7, min_periods=1).mean()
        

        denominador = hist_contexto['media_7dias_anterior_calc'] + 1e-6
        hist_contexto['crescimento_percentual_calc'] = ((hist_contexto['media_7dias_calc'] - hist_contexto['media_7dias_anterior_calc']) / denominador) * 100
        
       
        ultimo_registro = hist_contexto.iloc[-1]
        features['media_3dias'] = ultimo_registro.get('media_3dias_calc', 0)
        features['crescimento_percentual'] = ultimo_registro.get('crescimento_percentual_calc', 0)
    else:
        
        features['media_3dias'] = 0
        features['crescimento_percentual'] = 0

   
    for key in ['media_3dias', 'crescimento_percentual']:
        if pd.isna(features[key]):
            features[key] = 0

    return features




media_risco_ocorrencia = df_historico['risco_ocorrencia'].mean()
anomalias_cameras = df_historico['anomalias_cameras_ultimas_24h'].mean()

st.title("Cidade Segura - Previsão de Risco e Reforços")

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Média de Risco de Ocorrência (Histórico)", value=f"{media_risco_ocorrencia:.2f}%")
    with col2:
        st.metric(label="Média de anomalias detectadas nas câmeras por dia", value=f"{anomalias_cameras:.2f}%")


with st.container(border=True):
    st.subheader("Análise Histórica de Risco")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Ocorrência por Dia da Semana")
        grouped_data = df_historico.groupby('dia_da_semana')['risco_ocorrencia'].count()
        st.line_chart(grouped_data)

    with col2:
        st.markdown("##### Ocorrência por Mês")
        grouped_data_dois = df_historico.groupby('mes')['risco_ocorrencia'].count()
        st.bar_chart(grouped_data_dois)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("##### Ocorrência por Zona")
        grouped_data_seis = df_historico.groupby('zona')['risco_ocorrencia'].count().sort_values(ascending=False)
        st.bar_chart(grouped_data_seis)

    with col4:
        st.markdown("##### Ocorrência por Tipo de Ocorrência")
        grouped_data_sete = df_historico.groupby('tipo_ocorrencia')['risco_ocorrencia'].count().sort_values(ascending=False)
        st.bar_chart(grouped_data_sete)



st.subheader("Gerar Previsão de Risco e Reforços")
st.markdown("""
    Insira as informações solicitadas abaixo para que o modelo possa prever o risco de ocorrência e 
    recomendar a alocação de recursos.
""")

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        zona = st.selectbox('Selecione a Região/Zona', sorted(df_historico['zona'].unique()))
    with col2:
        tipo_ocorrencia = st.selectbox('Tipo de Ocorrência', sorted(df_historico['tipo_ocorrencia'].unique()))

    col3, col4 = st.columns(2)
    with col3:
        data = st.date_input('Selecione a Data para Previsão', value=datetime.now())
    with col4:
        faixa_horaria = st.selectbox('Faixa Horária', ['00-06h', '06-12h', '12-18h', '18-00h'])

    col5, col6 = st.columns(2)
    with col5:
        clima = st.selectbox('Condição Climática', ['Céu limpo', 'Nublado', 'Chuva', 'Outro'])
    with col6:
        evento_especial = st.selectbox('Evento Especial na Região?', ['Sim', 'Não'])

    col7, col8 = st.columns(2)
    with col7:
        denuncias_app_ultimas_24h = st.number_input('Número de denúncias (últimas 24h)', min_value=0, value=5)
    with col8:
        anomalias_cameras_ultimas_24h = st.number_input('Anomalias detectadas (últimas 24h)', min_value=0, value=3)

    if st.button('Gerar Previsão', type="primary", use_container_width=True):
        with st.spinner('Calculando features e fazendo a previsão...'):
            
            
            features_calculadas = gerar_features_dinamicas(
                df_historico=df_historico,
                zona_selecionada=zona,
                tipo_ocorrencia_selecionado=tipo_ocorrencia,
                data_previsao=data
            )

            
            input_data = pd.DataFrame({
          
                'zona': [zona],
                'tipo_ocorrencia': [tipo_ocorrencia],
                'clima': [clima],
                'evento_especial': [evento_especial],
                'faixa_horaria': [faixa_horaria], 
                'denuncias_app_ultimas_24h': [denuncias_app_ultimas_24h],
                'anomalias_cameras_ultimas_24h': [anomalias_cameras_ultimas_24h],
                
          
                **features_calculadas
            })

            
            input_data = pd.get_dummies(input_data)
            model_columns = model.feature_names_in_
            input_data = input_data.reindex(columns=model_columns, fill_value=0)

          
            prediction_result = model.predict(input_data)
            risco_previsto = prediction_result[0] if isinstance(prediction_result[0], (int, float)) else prediction_result[0][0]


           
            if risco_previsto >= 55:
                viaturas_recomendadas = 4
            elif risco_previsto >= 30:
                viaturas_recomendadas = 3
            elif risco_previsto >= 25:
                viaturas_recomendadas = 2
            else:
                viaturas_recomendadas = 1
            
         
            st.success(f'**Risco estimado de ocorrência: {risco_previsto:.1f}%**')
            st.info(f'**Recomendação de reforço: {viaturas_recomendadas} viaturas extras**')

