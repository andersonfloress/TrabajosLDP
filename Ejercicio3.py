import streamlit as st

entrada = ('Precios.txt') 
conversion = 3.85
p_convertidos = []

try:
    with open(entrada, 'r') as archivo:
        for line in archivo:
            partes = line.strip().split(', ')
            producto = partes[0]
            p_dolar = float(partes[1])
            p_soles = p_dolar * conversion
            resultado = f'{producto}, {p_soles:.2f}'
            p_convertidos.append(resultado)

    st.title('Conversion de Dolares a Soles')
    if p_convertidos:
        st.subheader('Resultados de la conversion')
        for resultado in p_convertidos:
            st.write(resultado)

        salida = '\n'.join(p_convertidos)

        st.download_button('Descargar Archivo', salida, file_name='precios en soles.txt')
    else:
        st.info(f'No se encontraron datos en el archivo {entrada}')   
except FileNotFoundError:
    st.error(f'El archivo {entrada} no existe') 