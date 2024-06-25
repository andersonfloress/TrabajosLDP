import random
import time
import streamlit as st
import pandas as pd
import plotly.express as px

def busqueda_lineal(array, numero):
    inicio_busqueda= time.time()
    iteraciones = 0
    for i in range(len(array)):
        iteraciones += 1
        if array[i] == numero:
            fin_busqueda = time.time()
            return i, inicio_busqueda, fin_busqueda, iteraciones
    fin_busqueda = time.time()
    return -1, inicio_busqueda, fin_busqueda, iteraciones

st.title("Búsqueda Lineal")

num_ejecuciones = st.number_input("Ingrese el número de ejecuciones:", 
                                  min_value=1, max_value=10000, value=50, step=1)
tamaño_inicial = 10
incremento = 100

resultados = []

for i in range(num_ejecuciones):
    tamaño_array = tamaño_inicial + (i * incremento)
    
    inicio_ejecucion = time.time()
    array = [random.randint(0, 100) for _ in range(tamaño_array)]
    num_buscar = random.randint(0, 100)
    fin_generacion = time.time()
    
    posicion, inicio_busqueda, fin_busqueda, iteraciones = busqueda_lineal(array, num_buscar)
    fin_ejecucion = time.time()
    
    resultado = {
        'Ejecucion': i + 1,
        'Numero a Buscar': num_buscar,
        'Posicion': posicion,
        'Tiempo de Inicio': inicio_busqueda,
        'Tiempo de Fin': fin_busqueda,
        'Tiempo Total': fin_busqueda - inicio_busqueda,
        'Tiempo de Ejecucion del Array': fin_ejecucion - inicio_ejecucion,
        'Numero de  Iteraciones': iteraciones,
        'Tamano del Array': tamaño_array
    }
    resultados.append(resultado)

df_resultados = pd.DataFrame(resultados)

st.subheader("Resultados")
st.write(df_resultados.to_html(index=False), unsafe_allow_html=True)

st.subheader("Gráfico del Tamaño del Array - Tiempo Total")
fig = px.line(df_resultados, x='Tamano del Array', y='Tiempo Total', 
              title='Tamaño del array - Tiempo Total',
              labels={'Tamano del Array': 'Tamaño del array', 
                      'Tiempo Total': 'Tiempo Total (segundos)'})
st.plotly_chart(fig)
