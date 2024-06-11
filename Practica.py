import pandas as pd
import streamlit as st

class DataHandler:
    def __init__(self, archivo):
        self.archivo = archivo
        self.datos = None

    def cargar_datos(self):
        self.datos = pd.read_csv(self.archivo)

    def vista_datos(self):
        return self.datos.head(10)

    def calculos_estadisticos(self):
        columnas_excluidas = [col for col in self.datos.columns if 'id' in col.lower() or col in ['FECHA', 'FECHA_CORTE']]
        datos_numericos = self.datos.drop(columns=columnas_excluidas).select_dtypes(include=['float64', 'int64'])
        
        media = datos_numericos.mean()
        mediana = datos_numericos.median()
        desv_std = datos_numericos.std()
        return pd.DataFrame({
            'Media': media,
            'Mediana': mediana,
            'Desviacion Estandar': desv_std
        })

def main():
    st.title("Analisis de Datos")

    archivo_cargado = st.file_uploader("Cargar archivo CSV", type=["csv"])
    if archivo_cargado is not None:
        data_handler = DataHandler(archivo_cargado)
        data_handler.cargar_datos()

        st.subheader("Visualizacion de datos")
        st.write(data_handler.vista_datos())

        st.subheader("Analisis estadistico")
        estatisticas = data_handler.calculos_estadisticos()
        st.write("Estadisticas descriptivas:")
        st.write(estatisticas)

if __name__ == "__main__":
    main()
