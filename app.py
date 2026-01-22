import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

# ---- CONFIGURACIÓN DE PÁGINA ----
st.set_page_config(
    page_title="Tarym Hernandez Hair Care",
    page_icon="💧",
    layout="centered"
)

# ---- ESTILOS ----
st.markdown("""
<style>
body { background-color: #f6eff4; }
h1, h2, h3 { color: #c2a15f; }
section[data-testid="stSidebar"] { background-color: #f1e7ec; }
</style>
""", unsafe_allow_html=True)

# ---- LOGO ----
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=220)
else:
    st.warning("Logo no encontrado")

st.markdown("<h2 style='text-align:center;'>Tratamiento de Aminoácidos Capilares</h2>", unsafe_allow_html=True)

# ---- BASE DE DATOS ----
db_path = os.path.join(os.path.dirname(__file__), "clientas.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS clientas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    telefono TEXT,
    email TEXT,
    instagram TEXT,
    tipo_cabello TEXT,
    fecha_procedimiento TEXT,
    proxima_cita TEXT
)
""")
conn.commit()

def calcular_proxima(fecha):
    return fecha + relativedelta(months=5)

# ---- MENÚ ----
menu = st.sidebar.selectbox("Menú", ["Registro", "Calendario", "Admin", "Notificaciones"])

# ---- REGISTRO ----
if menu == "Registro":
    st.subheader("Registro de clienta")

    nombre = st.text_input("Nombre")
    telefono = st.text_input("Teléfono")
    email = st.text_input("Email (opcional)")
    instagram = st.text_input("Usuario de Instagram (opcional)")
    tipo = st.selectbox("Tipo de cabello", ["Seco", "Graso", "Mixto", "Normal"])
    fecha = st.date_input("Fecha del procedimiento")

    if st.button("Guardar"):
        if nombre and telefono:
            prox = calcular_proxima(datetime.combine(fecha, datetime.min.time()))
            c.execute(
                "INSERT INT


