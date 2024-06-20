import streamlit as st
import math
from collections import Counter
import pandas as pd

def calcular_entropia(texto):
    frecuencia = Counter(texto)
    total_caracteres = len(texto)
    
    entropia = 0
    for char, count in frecuencia.items():
        probabilidad = count / total_caracteres
        entropia -= probabilidad * math.log2(probabilidad)
    
    return entropia, frecuencia

st.title("Calculadora de Entropia")

archivo_subido = st.file_uploader("Sube un archivo de texto", type="txt")

if archivo_subido is not None:
    contenido = archivo_subido.read().decode("utf-8")
    
    st.subheader("Contenido del archivo:")
    st.text(contenido)
    
    entropia, frecuencia = calcular_entropia(contenido)
    
    st.subheader("Caracteres:")
    frecuencia_df = pd.DataFrame(frecuencia.items(), columns=['Caracter', 'Repeticion'])
    st.table(frecuencia_df)
    
    st.subheader("Entropia del archivo:")
    st.write(entropia)
    
    resultado = f"Entropia: {entropia}"
    st.download_button("Descargar resultado", resultado, "output.txt")
