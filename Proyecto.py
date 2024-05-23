import streamlit as st
import sqlite3
from datetime import datetime, timedelta
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

def agregar_cita(nombre, fecha, hora_inicio, tipo_cita):
    hora_fin = (datetime.strptime(hora_inicio, '%H:%M') + timedelta(hours=1)).strftime('%H:%M')
    if not verificar_horario(fecha, hora_inicio, hora_fin):
        with conexion() as conn:
            conn.execute('''
                INSERT INTO citas (nombre, fecha, hora_inicio, hora_fin, tipo_cita)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, fecha, hora_inicio, hora_fin, tipo_cita))
            return conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    return None

def verificar_horario(fecha, hora_inicio, hora_fin):
    with conexion() as conn:
        solapamientos = conn.execute('''
            SELECT COUNT(*)
            FROM citas
            WHERE fecha = ? AND ((hora_inicio < ? AND hora_fin > ?) OR (hora_inicio < ? AND hora_fin > ?))
        ''', (fecha, hora_fin, hora_inicio, hora_inicio, hora_fin)).fetchone()[0]
    return solapamientos > 0

def cancelar_cita(cita_id):
    with conexion() as conn:
        conn.execute('DELETE FROM citas WHERE id = ?', (cita_id,))
    return f'Cita {cita_id} cancelada'

def obtener_citas_por_tipo(tipo_cita):
    with conexion() as conn:
        return conn.execute('''
            SELECT id, nombre, fecha, hora_inicio, hora_fin
            FROM citas
            WHERE tipo_cita = ?
            ORDER BY fecha, hora_inicio
        ''', (tipo_cita,)).fetchall()

crear_tabla()

st.title('Programación de Citas Médicas')
st.sidebar.header('Registrar una nueva cita')

tipos_cita = ['Pediatría', 'Odontología', 'Ginecología', 'Urología', 'Geriatría', 'Preventiva', 
              'Control o Seguimiento', 'Cardiología', 'Endocrinología', 'Psicología', 'Toxicología']

with st.sidebar.form(key='formulario_cita'):
    nombre = st.text_input('Nombre del paciente')
    fecha = st.date_input('Fecha de la cita')
    hora_inicio = st.time_input('Hora de la cita')
    tipo_cita = st.selectbox('Tipo de cita', tipos_cita)
    boton_submit = st.form_submit_button(label='Registrar Cita')

if boton_submit:
    cita_id = agregar_cita(nombre, fecha.strftime('%d-%m-%Y'), hora_inicio.strftime('%H:%M'), tipo_cita)
    if cita_id:
        mensaje_exito = 'Cita registrada exitosamente'
        mensaje_temporal = st.empty()
        mensaje_temporal.success(mensaje_exito)
        time.sleep(2)
        mensaje_temporal.empty()
    else:
        st.sidebar.error('Ya existe una cita en ese horario')

st.header('Citas Médicas Programadas:')
for tipo in tipos_cita:
    citas_tipo = obtener_citas_por_tipo(tipo)
    if citas_tipo:
        st.subheader(tipo)
        for cita in citas_tipo:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"Paciente: {cita[1]}, Fecha: {cita[2]}, Hora: {cita[3]} - {cita[4]}")
            with col2:
                if st.button(f'Cancelar cita', key=f'cancel_{cita[0]}'):
                    st.success(cancelar_cita(cita[0]))
                    st.experimental_rerun()
