import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.title("Análise SELIC - Resultado dos Leilões")

# URL da API do Banco Central para a série da SELIC diária
url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json"

# Fazer a requisição HTTP para obter os dados
response = requests.get(url)

# Verificar o status da resposta
if response.status_code == 200:
    try:
        # Converter os dados para um DataFrame
        dados = response.json()
        tabela = pd.DataFrame(dados)

        # Converter a coluna 'data' para datetime
        tabela['data'] = pd.to_datetime(tabela['data'], format='%Y-%m-%d')

        # Converter a coluna 'valor' para float
        tabela['valor'] = tabela['valor'].astype(float)

        # Renomear colunas para facilitar a leitura
        tabela.rename(columns={'data': 'Data', 'valor': 'Taxa SELIC'}, inplace=True)

        # Ordenar os dados por data
        tabela.sort_values(by='Data', inplace=True)

        # Criar um filtro para selecionar a coluna desejada
        colunas = ['Taxa SELIC']
        cores = ['green']
        coluna_selecionada = st.selectbox("Selecione o dado para análise:", colunas)

        # Obter a cor correspondente à coluna selecionada
        cor_selecionada = cores[colunas.index(coluna_selecionada)]

        # Gráfico de linha para a coluna selecionada
        st.write(f"### {coluna_selecionada}")
        fig = px.line(
            tabela,
            x='Data',
            y=coluna_selecionada,
            title=f"Análise - {coluna_selecionada}",
            labels={'Data': 'Data', coluna_selecionada: 'Valor'}
        )
        fig.update_traces(line_color=cor_selecionada)
        st.plotly_chart(fig, use_container_width=True)

        # Calcular e exibir a variação percentual mensal (MoM) para a coluna selecionada
        st.write(f"### Variação Percentual Mensal (MoM) - {coluna_selecionada}")
        tabela[f'{coluna_selecionada}_MoM'] = tabela[coluna_selecionada].pct_change() * 100
        mom_data = pd.DataFrame({'Data': tabela['Data'], 'MoM Change (%)': tabela[f'{coluna_selecionada}_MoM']})

        fig_mom = px.bar(
            mom_data,
            x='Data',
            y='MoM Change (%)',
            title=f"Variação Percentual Mensal (MoM) - {coluna_selecionada}",
            labels={'Data': 'Data', 'MoM Change (%)': 'Variação (%)'}
        )
        fig_mom.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
        st.plotly_chart(fig_mom, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")

else:
    st.error(f"Erro ao acessar o site: {response.status_code}. Verifique a URL ou tente novamente mais tarde.")