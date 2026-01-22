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
            # Línea corregida: INSERT INTO completa y cerrada
            c.execute(
                "INSERT INTO clientas VALUES (NULL,?,?,?,?,?,?,?)",
                (nombre, telefono, email, instagram, tipo, fecha.strftime("%Y-%m-%d"), prox.strftime("%Y-%m-%d"))
            )
            conn.commit()
            st.success(f"Guardado. Próxima cita: {prox.strftime('%d-%m-%Y')}")
        else:
            st.error("Nombre y teléfono son obligatorios")

# ---- CALENDARIO ----
elif menu == "Calendario":
    st.subheader("Próximas citas")
    df = pd.read_sql("SELECT nombre, telefono, proxima_cita FROM clientas", conn)
    st.dataframe(df)

# ---- ADMIN ----
elif menu == "Admin":
    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if user == "admin" and pwd == "1234":
            st.success("Acceso concedido")
            df = pd.read_sql("SELECT * FROM clientas", conn)
            st.dataframe(df)
        else:
            st.error("Credenciales incorrectas")

# ---- NOTIFICACIONES 4 MESES ----
elif menu == "Notificaciones":
    st.subheader("Clientas próximas a cumplir 4 meses desde su tratamiento")

    df = pd.read_sql("SELECT nombre, telefono, email, instagram, fecha_procedimiento, proxima_cita FROM clientas", conn)
    hoy = datetime.today().date()

    notificaciones = []
    for _, row in df.iterrows():
        fecha_proc = datetime.strptime(row['fecha_procedimiento'], "%Y-%m-%d").date()
        diferencia = (hoy - fecha_proc).days
        # Aproximadamente 4 meses = 120 días
        if 118 <= diferencia <= 122:
            notificaciones.append({
                "Nombre": row['nombre'],
                "Teléfono": row['telefono'],
                "Email": row['email'],
                "Instagram": row['instagram'],
                "Fecha de tratamiento": fecha_proc.strftime('%d-%m-%Y'),
                "Próxima cita": row['proxima_cita']
            })

    if notificaciones:
        st.dataframe(pd.DataFrame(notificaciones))
        st.info("Estas clientas están por cumplir 4 meses desde su tratamiento. ¡Es hora de contactarlas!")
    else:
        st.success("No hay clientas próximas a cumplir 4 meses.")



