import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.title("Análise de Investidores - B3")

# URL do site para os dados
url = "https://www.dadosdemercado.com.br/fluxo"

# Fazer a requisição HTTP para obter o conteúdo da página
response = requests.get(url)

# Verificar o status da resposta
if response.status_code == 200:
    # Ler os dados da tabela
    tabela = pd.read_html(response.content)[0]

    # Garantir que a coluna 'Data' esteja no formato datetime
    tabela['Data'] = pd.to_datetime(tabela['Data'], format='%d/%m/%Y', errors='coerce')

    # Tratar as colunas de valores (remover 'mi', ajustar separadores e converter para float)
    for coluna in ['Estrangeiro', 'Institucional', 'Pessoa física', 'Inst. Financeira', 'Outros']:
        tabela[coluna] = tabela[coluna].astype(str).str.replace(' mi', '', regex=False)
        tabela[coluna] = tabela[coluna].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

    # Ordenar os dados por data
    tabela.sort_values(by='Data', inplace=True)

    # Exibir os dados mais recentes no console
    st.write("### Dados mais recentes:")
    st.dataframe(tabela.tail())

    # Criar gráficos para cada coluna
    colunas = ['Estrangeiro', 'Institucional', 'Pessoa física', 'Inst. Financeira', 'Outros']
    cores = ['green', 'blue', 'orange', 'purple', 'red']

    for coluna, cor in zip(colunas, cores):
        st.write(f"### {coluna}")
        fig = px.line(
            tabela,
            x='Data',
            y=coluna,
            title=f"Fluxo de Investidores - {coluna}",
            labels={'Data': 'Data', coluna: 'Valor (R$ mi)'}
        )
        fig.update_traces(line_color=cor)
        st.plotly_chart(fig, use_container_width=True)

    # Calcular e exibir a variação percentual mensal (MoM) para cada coluna
    st.write("### Variação Percentual Mensal (MoM)")
    for coluna in colunas:
        tabela[f'{coluna}_MoM'] = tabela[coluna].pct_change() * 100
        mom_data = pd.DataFrame({'Data': tabela['Data'], 'MoM Change (%)': tabela[f'{coluna}_MoM']})

        fig_mom = px.bar(
            mom_data,
            x='Data',
            y='MoM Change (%)',
            title=f"Variação Percentual Mensal (MoM) - {coluna}",
            labels={'Data': 'Data', 'MoM Change (%)': 'Variação (%)'}
        )
        fig_mom.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
        st.plotly_chart(fig_mom, use_container_width=True)

else:
    st.write(f"Erro ao acessar o site: {response.status_code}")