import streamlit as st
from collections import defaultdict

entrada = 'Errores.txt'
Errores = defaultdict(int)

try:
    with open(entrada, 'r') as archivo:
        for line in archivo:
            error = line.split(':')[0].strip()
            Errores[error] += 1

    resultado = [f'{error}: {cantidad}'for error, cantidad in Errores.items()]
    
    salida = '\n'.join(resultado)
    st.title('Resumen de Errores')
    st.subheader('Errores:')
    for line in resultado:
        st.write(line)

    st.download_button('Descargar Archivo', salida.encode('utf-8'), file_name='Resumen de errores.txt')

except FileNotFoundError:
    st.error(f'El archivo {entrada} no existe')