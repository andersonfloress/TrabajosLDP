import streamlit as st

entrada = 'Ventas.txt'
ventas = []
total = 0
v_max = ''
v_min = ''

try:
    with open(entrada, 'r') as archivo:
        for line in archivo:
            partes = line.strip().split(', ')
            dia = partes[0]
            monto = int(partes[1])
            ventas.append((dia, monto))
            total += monto

            if not v_max or monto > v_max[1]:
                v_max = (dia, monto)

            if not v_min or monto < v_min[1]:
                v_min = (dia, monto)

    promedio = total / len(ventas) if ventas else 0

    total_str = f'Vental Total: {total}'
    promedio_str = f'Promedio de Ventas: {promedio:.2f}'
    v_max_str = f'Dia de Mayor Venta: {v_max[0]}, {v_max[1]}'
    v_min_str = f'Dia de Menor Venta: {v_min[0]}, {v_min[1]}'

    st.title('Ventas Diarias')
    st.subheader('Resultados:')
    st.write(total_str)
    st.write(promedio_str)
    st.write(v_max_str)
    st.write(v_min_str)

    salida = f'{total_str}\n{promedio_str}\n{v_max_str}\n{v_min_str}'

    st.download_button('Descargar Archivo',salida.encode('utf-8'),file_name='P de ventas.txt')

except FileNotFoundError:
    st.error(f'El archivo {entrada} no existe')