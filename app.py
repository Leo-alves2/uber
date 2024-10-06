# IMPORTAR BIBLIOTECAS
import streamlit as st
import pandas as pd
import numpy as np

# CONFIGURAÇÃO DA PAGINA

DATA_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# DEFINIR TITULO

st.title('Uber dados de NY')

# DEFINIR FUNÇAO PARA CARREGAR OS DADOS

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows= nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis= 'columns', inplace= True)
    data[DATA_COLUMN] = pd.to_datetime(data[DATA_COLUMN])
    return data

# CHAMAR A FUNÇÃO PARA CARREGAR OS DADOS
data_load_state = st.text('Carregando dados...')
data = load_data(1000)
data_load_state = st.text('Dados carregados...') 
# st.dataframe(data)

# data.info()

# PERMITIR O VISUALIZAÇÃO DOS DADOS BRUTOS

if st.checkbox('Visualizar os dados'):
    st.subheader('Raw data')
    st.dataframe(data)

# CRIAR GRAFICOS

st.subheader('Numero de embarque por hora')

hist_values = np.histogram(data[DATA_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# FILTRAR DATASET

hour_to_filter = st.slider('hour', 0, 23, 17)
filtro_data = data[data[DATA_COLUMN].dt.hour == hour_to_filter]

# MOSTRAR LOCALIZAÇÃO

st.subheader(f'Map de embarque e hora {hour_to_filter}:00')
st.map(filtro_data)