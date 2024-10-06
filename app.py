# IMPORTAR BIBLIOTECAS
import streamlit as st  # Usada para criar a aplicação web interativa
import pandas as pd     # Usada para manipulação e análise de dados
import numpy as np      # Usada para cálculos numéricos e criação de gráficos

# CONFIGURAÇÃO DA PÁGINA
# URL do dataset de exemplo da Uber em Nova York (setembro de 2014)
DATA_COLUMN = 'date/time'  
DATA_URL = ('https://s3-us-west-2.amazonaws.com/' 
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# DEFINIR TÍTULO
st.title('Uber dados de NY')  # Define o título da página

# DEFINIR FUNÇÃO PARA CARREGAR OS DADOS
# A função abaixo carrega os dados a partir de um CSV e faz a conversão de colunas para minúsculas
# O decorador `@st.cache_data` ajuda a otimizar o carregamento dos dados em cache
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)  # Lê o CSV com um número limitado de linhas
    lowercase = lambda x: str(x).lower()       # Função lambda para converter colunas para minúsculas
    data.rename(lowercase, axis='columns', inplace=True)  # Aplica a função lambda nos nomes das colunas
    data[DATA_COLUMN] = pd.to_datetime(data[DATA_COLUMN]) # Converte a coluna de data/hora para o formato datetime
    return data

# CHAMAR A FUNÇÃO PARA CARREGAR OS DADOS
data_load_state = st.text('Carregando dados...')  # Exibe mensagem enquanto os dados estão carregando
data = load_data(1000)  # Carrega os primeiros 1000 registros do dataset
data_load_state = st.text('Dados carregados...')  # Atualiza a mensagem ao concluir o carregamento

# VISUALIZAR OS DADOS BRUTOS
# Se o usuário selecionar a caixa de seleção, os dados brutos serão exibidos
if st.checkbox('Visualizar os dados'):
    st.subheader('Dados Brutos')  # Subtítulo para a seção de dados
    st.dataframe(data)            # Exibe os dados brutos como um dataframe

# CRIAR GRÁFICOS
# Gera um histograma que mostra o número de embarques por hora
st.subheader('Número de embarques por hora')  # Subtítulo para o gráfico
hist_values = np.histogram(data[DATA_COLUMN].dt.hour, bins=24, range=(0, 24))[0]  # Calcula o histograma
st.bar_chart(hist_values)  # Exibe o gráfico de barras

# FILTRAR DATASET POR HORA
# Usa um controle deslizante para permitir que o usuário selecione a hora que deseja visualizar
hour_to_filter = st.slider('Selecione a hora', 0, 23, 17)  # Controle deslizante (slider)
filtro_data = data[data[DATA_COLUMN].dt.hour == hour_to_filter]  # Filtra os dados pela hora selecionada

# EXIBIR O MAPA COM LOCAIS DE EMBARQUE
# Mostra um mapa com os locais de embarque para a hora selecionada
st.subheader(f'Mapa de embarques às {hour_to_filter}:00')  # Subtítulo do mapa
st.map(filtro_data)  # Exibe o mapa com base nos dados filtrados