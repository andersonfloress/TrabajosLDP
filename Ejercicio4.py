import streamlit as st

entrada = 'Temperaturas.txt'
t_max = -100
t_min = 99999
r_max = ''
r_min = ''
try:
    with open(entrada, 'r') as archivo:
        for line in archivo:
            partes = line.strip().split(', ')
            dia = partes[0]
            temperatura = float(partes[1])
            
            if temperatura > t_max:
                t_max = temperatura
                r_max = f'Dia de Temperatura maxima: {dia},{ temperatura}'
        
            if temperatura < t_min:
                t_min = temperatura
                r_min = f'Dia de Temperatura minima: {dia },{ temperatura}'
    st.title('Registro de Temperaturas')
    
    st.subheader('Registro:')
    st.write(r_max)
    st.write(r_min)

    salida = f'{r_max}\n{r_min}'

    st.download_button('Descargar Archivo', salida.encode('utf-8'), file_name='Registo de T.txt')
        
except FileNotFoundError:
    st.error(f'El archivo {entrada} no existe')