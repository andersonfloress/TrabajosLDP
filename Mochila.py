import streamlit as st

def calcular_viajes(pesos, peso_maximo):
    viajes = 0
    objetos_no_cargados = []

    while pesos:
        peso_actual = 0
        for peso in sorted(pesos, reverse=True):
            if peso > peso_maximo:
                objetos_no_cargados.append(peso)
                pesos.remove(peso)
            elif peso_actual + peso <= peso_maximo:
                peso_actual += peso
                pesos.remove(peso)
        if peso_actual > 0:
            viajes += 2 
    return viajes, objetos_no_cargados

st.title('Problema de la Mochila: Cálculo de Viajes')

peso_maximo = st.number_input('PESO MAXIMO DE LA MOCHILA:', min_value=0.0, step=0.1)
num_objetos = st.number_input('NUMERO DE OBJETOS:', min_value=1, step=1)
pesos_input = st.text_area('Ingrese los pesos de los objetos separados por comas:', '')

if st.button('Calcular Viajes'):
    try:
        pesos = [float(peso.strip()) for peso in pesos_input.split(',')]
        if len(pesos) != num_objetos:
            st.error('El número de pesos ingresados no coincide con el número de objetos.')
        else:
            viajes, objetos_no_cargados = calcular_viajes(pesos, peso_maximo)
            st.write(f'La cantidad de viajes fue: {viajes}')

            if objetos_no_cargados:
                st.warning("Algunos objetos no pudieron ser cargados debido a que su peso supera la capacidad de la mochila.")
                for peso in objetos_no_cargados:
                    st.warning(f"Un objeto con peso {peso} supera la capacidad de la mochila.")
    except ValueError:
        st.error('Por favor, ingrese los pesos correctamente como números separados por comas.')
