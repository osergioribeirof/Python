import streamlit as st
import pandas as pd
import yfinance as yf 
    

st.write(""" # BCB - DADOS ECONÔMICOS DO BRASIL """)

#VOLUME SERVICES

import requests
import pandas as pd
from io import StringIO

# URL da API para o código 23982
url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.23982/dados?formato=json"

# Fazer a requisição
response = requests.get(url)

# Verificar o status da resposta
if response.status_code == 200:
    # Converter os dados para um DataFrame usando StringIO
    VolumeServices = pd.read_json(StringIO(response.text))
    VolumeServices['data'] = pd.to_datetime(VolumeServices['data'], format='%d/%m/%Y')
    VolumeServices.set_index('data', inplace=True)
    
    # Exibir as datas mais recentes
    print("Dados mais recentes:")
    print(VolumeServices.tail())  # Exibe as últimas 5 linhas do DataFrame
else:
    print(f"Erro ao acessar a API: {response.status_code}")
    
 # CRIAR O GRÁFICO VOLUME SERVICES
 
 st.line_chart(VolumeServices, use_container_width=True)
 #st.write(VolumeServices)
    
