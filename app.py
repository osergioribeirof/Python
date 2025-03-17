import streamlit as st
import BCB_Dados_Econômicos_do_Brasil_  # Importa o código com o gráfico

st.title("Gráfico do BCB - Volume Services")

# Chama a função do outro arquivo
figura = BCB_Dados_Econômicos_do_Brasil_.volumeservices()

# Verifica se a função retornou um gráfico válido
if figura:
    st.pyplot(figura)  # Exibe o gráfico no Streamlit
else:
    st.error("Erro: volumeservices() não retornou um gráfico válido.")
    
    