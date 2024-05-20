import streamlit as st

entrada = 'Calcular promedio.txt'
promedios = [] 

try:
    with open(entrada, 'r') as archivo: 
        lines = archivo.readlines()
        for line in lines:
            partes = line.strip().split(', ')
            nombre = partes[0]
            notas = [int(curso.split(': ')[1]) for curso in partes[1:]]
            prom = sum(notas) / len(notas)
            
            resultado = f'{nombre}, Promedio: {prom:.2f}'
            promedios.append(resultado)

    st.title('Promedios de Notas')      
    if promedios:
        st.subheader('Resultados de Promedios:')
        for resultado in promedios:
            st.write(resultado)

        salida = '\n'.join(promedios)
        
        st.download_button('Desacargar Archivo', salida, file_name='Promedios.txt')
    else:
        st.info(f'No se encontraron datos en el archivo {entrada}.')

except FileNotFoundError:
    st.error(f'El archivo {entrada} no existe')        