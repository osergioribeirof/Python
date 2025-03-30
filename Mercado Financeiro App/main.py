import streamlit as st
import pandas as pd
import yfinance as yf 
    

st.write(""" # BCB - DADOS ECONÔMICOS DO BRASIL """)

#VOLUME SERVICES

import streamlit as st
import pandas as pd
import requests

st.write("""# BCB - DADOS ECONÔMICOS DO BRASIL""")

# VOLUME SERVICES

# URL da API para o código 23982
url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.23982/dados?formato=json"

# Fazer a requisição
response = requests.get(url)

# Verificar o status da resposta
if response.status_code == 200:
    # Converter os dados para um DataFrame diretamente do JSON
    VolumeServices = pd.DataFrame(response.json())
    VolumeServices['data'] = pd.to_datetime(VolumeServices['data'], format='%d/%m/%Y')
    VolumeServices.set_index('data', inplace=True)
    
    # Ordenar os dados por data
    VolumeServices.sort_index(inplace=True)
    
    # Exibir as datas mais recentes no console
    print("Dados mais recentes:")
    print(VolumeServices.tail())  # Exibe as últimas 5 linhas do DataFrame
    
    # Criar o gráfico no Streamlit
    st.line_chart(VolumeServices['valor'])  # Exibe a coluna 'valor' ordenada
else:
    st.write(f"Erro ao acessar a API: {response.status_code}")