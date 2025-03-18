import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Exemplo de gráfico
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title('Sine Wave')

# Exibir no Streamlit
st.pyplot(plt)

