import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.title("Análise SELIC - Resultado dos Leilões")

# URL do site para os dados SELIC
url = "https://www.dadosdemercado.com.br/selic"

# Adicionar cabeçalhos à requisição
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Fazer a requisição HTTP para obter o conteúdo da página
response = requests.get(url, headers=headers)

# Verificar o status da resposta
if response.status_code == 200:
    try:
        # Ler os dados da tabela
        tabela = pd.read_html(response.content)[0]

        # Garantir que a coluna 'Data' esteja no formato datetime
        tabela['Data'] = pd.to_datetime(tabela['Data'], format='%d/%m/%Y', errors='coerce')

        # Tratar as colunas de valores (remover 'mi', ajustar separadores e converter para float)
        for coluna in ['Taxa SELIC', 'Volume Ofertado', 'Volume Aceito']:
            tabela[coluna] = tabela[coluna].astype(str).str.replace(' mi', '', regex=False)
            tabela[coluna] = tabela[coluna].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

        # Ordenar os dados por data
        tabela.sort_values(by='Data', inplace=True)

        # Criar um filtro para selecionar a coluna desejada
        colunas = ['Taxa SELIC', 'Volume Ofertado', 'Volume Aceito']
        cores = ['green', 'blue', 'orange']
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