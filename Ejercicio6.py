import streamlit as st
from collections import defaultdict

entrada = 'Horas trabajadas.txt'
h_totales =defaultdict(int)

try:
    with open(entrada, 'r') as archivo:
        for line in archivo:
            partes =line.strip().split(', ')
            nombre = partes[0]
            horas = int(partes[1])
            h_totales[nombre] += horas

    resultado = []
    for nombre, horas in h_totales.items():
        resultado.append(f'{nombre}, Horas Totales: {horas}')

    salida = '\n'.join(resultado)
    st.title('Registro de Horas Trabajadas por Empleado')
    st.subheader('Registro:') 
    for line in resultado:
        st.write(line)

    st.download_button('Descargar Archivo', salida.encode('utf-8'),file_name='Registro de horas.txt')

except FileNotFoundError:
    st.error(f'El archivo {entrada} no existe')              
