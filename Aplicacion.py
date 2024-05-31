import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

def conexion():
    return sqlite3.connect('Citas_medicas.db')

def crear_tabla():
    with conexion() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_fin TEXT NOT NULL,
                tipo_cita TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS citas_realizadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_fin TEXT NOT NULL,
                tipo_cita TEXT NOT NULL,
                fecha_realizacion TEXT NOT NULL
            )
        ''')

def verificar_horario_disponible(fecha, hora_inicio, hora_fin, tipo_cita):
    with conexion() as conn:
        hora_inicio_str = hora_inicio.strftime('%H:%M')
        hora_fin_str = hora_fin.strftime('%H:%M')

        query = '''
            SELECT COUNT(*)
            FROM citas
            WHERE fecha = ? 
            AND tipo_cita = ? 
            AND (
                (hora_inicio <= ? AND hora_fin > ?) OR
                (hora_inicio < ? AND hora_fin >= ?) OR
                (hora_inicio >= ? AND hora_fin <= ?)
            )
        '''
        result = conn.execute(query, (fecha.strftime('%Y-%m-%d'), tipo_cita, hora_inicio_str, hora_inicio_str, hora_fin_str, hora_fin_str, hora_inicio_str, hora_fin_str)).fetchone()

        return result[0] == 0

def agregar_cita(nombre, fecha, hora_inicio, hora_fin, tipo_cita):
    if not verificar_horario_disponible(fecha, hora_inicio, hora_fin, tipo_cita):
        mensaje_error = st.error('Horario no disponible')
        time.sleep(2)
        mensaje_error.empty()
        return

    with conexion() as conn:
        conn.execute('''
            INSERT INTO citas (nombre, fecha, hora_inicio, hora_fin, tipo_cita)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, fecha, hora_inicio.strftime('%H:%M'), hora_fin.strftime('%H:%M'), tipo_cita))
        mensaje_exito = st.success('Cita programada exitosamente')
        time.sleep(2)
        mensaje_exito.empty()

def mover_citas():
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with conexion() as conn:
        citas_vencidas = conn.execute('''
            SELECT *
            FROM citas
            WHERE fecha || ' ' || hora_fin <= ?
        ''', (ahora,)).fetchall()
        for cita in citas_vencidas:
            conn.execute('''
                INSERT INTO citas_realizadas (nombre, fecha, hora_inicio, hora_fin, tipo_cita, fecha_realizacion)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (cita[1], cita[2], cita[3], cita[4], cita[5], ahora))
            conn.execute('DELETE FROM citas WHERE id = ?', (cita[0],))

def obtener_citas_por_tipo(tipo_cita):
    with conexion() as conn:
        return conn.execute('''
            SELECT id, nombre, fecha, hora_inicio, hora_fin
            FROM citas
            WHERE tipo_cita = ?
            ORDER BY id
        ''', (tipo_cita,)).fetchall()

def cancelar_cita(cita_id):
    with conexion() as conn:
        conn.execute('DELETE FROM citas WHERE id = ?', (cita_id,))
    mensaje_cancelacion = st.success('Cita cancelada')
    time.sleep(2)
    mensaje_cancelacion.empty()

crear_tabla()
mover_citas()

st.markdown(
    """
    <style>
    .row_heading.level0 {display:none}
    .blank {display:none}
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Programación de Citas Médicas')
st.sidebar.header('Programar una nueva cita:')

tipos_cita = ['Pediatría', 'Ginecología', 'Urología', 'Preventiva',
              'Cardiología', 'Control o Seguimiento']

with st.sidebar.form(key='formulario_cita'):
    nombre = st.text_input('Nombre del paciente:')
    fecha = st.date_input('Fecha de la cita:')
    hora_inicio = st.time_input('Hora de inicio:')
    hora_fin = st.time_input('Hora que Termina:')
    tipo_cita = st.selectbox('Tipo de cita:', tipos_cita)
    boton_submit = st.form_submit_button(label='Registrar Cita')

if boton_submit:
    agregar_cita(nombre, fecha, hora_inicio, hora_fin, tipo_cita)

st.header('Citas Médicas Programadas:')
for tipo in tipos_cita:
    citas_tipo = obtener_citas_por_tipo(tipo)
    if citas_tipo:
        with st.expander(tipo):
            citas_datos = []
            for index, cita in enumerate(citas_tipo, start=1):
                fecha_datetime = datetime.strptime(cita[2], '%Y-%m-%d')
                citas_datos.append({
                    "Nº cita": index,
                    "Paciente": cita[1],
                    "Fecha": fecha_datetime.strftime('%d-%m-%Y'),
                    "Hora inicio": cita[3],
                    "Hora fin": cita[4]
                })
            
            df_citas = pd.DataFrame(citas_datos)
            st.table(df_citas)

st.sidebar.header('Cancelar una cita')
tipo_cita_cancelar = st.sidebar.selectbox('Seleccione el tipo de cita', tipos_cita)
citas_tipo_cancelar = obtener_citas_por_tipo(tipo_cita_cancelar)

if citas_tipo_cancelar:
    citas_options = {f"Nº {index} - Paciente: {cita[1]}": cita[0] for index, cita in enumerate(citas_tipo_cancelar, start=1)}
    cita_a_cancelar = st.sidebar.selectbox('Seleccione una cita para cancelar', list(citas_options.keys()))

    if st.sidebar.button('Cancelar'):
        cita_id = citas_options[cita_a_cancelar]
        cancelar_cita(cita_id)

st.header('Citas Médicas Realizadas:')
with st.expander('Ver Citas Realizadas'):
    with conexion() as conn:
        citas_realizadas = conn.execute('SELECT * FROM citas_realizadas ORDER BY fecha_realizacion DESC').fetchall()
        citas_realizadas_data = []
        for index, cita in enumerate(citas_realizadas, start=1):
            citas_realizadas_data.append({
                "Nº cita": index,
                "Paciente": cita[1],
                "Fecha": cita[2],
                "Hora inicio": cita[3],
                "Hora fin": cita[4],
                "Tipo cita": cita[5]
            })
        
        df_citas_realizadas = pd.DataFrame(citas_realizadas_data)
        st.table(df_citas_realizadas)

mostrar_grafico = st.button('Mostrar Gráfico de Citas Realizadas')

if mostrar_grafico:
    citas_realizadas_count = df_citas_realizadas['Tipo cita'].value_counts()
    citas_realizadas_count = citas_realizadas_count.reindex(tipos_cita, fill_value=0)

    plt.figure(figsize=(10, 6))
    plt.plot(citas_realizadas_count.index, citas_realizadas_count.values, marker='o', linestyle='-', color='b')
    plt.title('Cantidad de Citas Realizadas')
    plt.xlabel('Tipo de Cita')
    plt.ylabel('Cantidad de Citas')
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)
