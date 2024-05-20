import streamlit as st

entrada = 'Datos.txt'
correos = []
try:
    with open(entrada,'r') as archivo:
        lines = archivo.readlines()
        for line in lines:
            partes = line.strip().split(', ')
            nombre = partes[0]
            edad = int(partes[1])
            email = partes[2]
            if edad > 18:
                correos.append(email)

    st.title('Correos Electronicos de Mayores de 18 años')
    if correos:
        st.subheader('Correos:')
        for correo in correos:
            st.write(correo)

        salida = '\n'.join(correos)
        st.download_button('Descargar archivo', salida, file_name='correos.txt')
    else:
        st.info(f'No se encontraron datos en el archivo {entrada}.')

except FileNotFoundError:
    st.error(f'El archivo {entrada} no existe')
