# app.py — la parte visual: convierte el motor en una página web con
# formulario, en vez de tener que escribir los datos adentro del código.

import os
import streamlit as st

# En Streamlit Cloud la key se configura en Settings → Secrets (ahí no hay
# archivo .env), así que la copiamos a una variable de entorno para que
# motor.py la encuentre igual que en tu compu.
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

from motor import generar_recomendacion

st.set_page_config(page_title="RoomCraft AI", page_icon="🛋️")

st.title("🛋️ RoomCraft AI")
st.write(
    "Contanos cómo es el espacio que querés diseñar y te devolvemos una "
    "propuesta armada con IA: distribución, muebles, colores y más."
)

# st.form agrupa todas las preguntas: la IA recién se llama una vez,
# cuando apretás el botón — no en cada tecla que tocás.
with st.form("formulario"):
    tipo_ambiente = st.selectbox("Tipo de ambiente", ["Habitación", "Living", "Cocina", "Oficina", "Comedor"])
    dimensiones = st.number_input("Dimensiones (m²)", min_value=1, value=12)
    estilo = st.selectbox("Estilo", ["Minimalista", "Moderno", "Industrial", "Escandinavo", "Clásico"])
    presupuesto = st.number_input("Presupuesto (USD)", min_value=0, value=800)
    colores = st.text_input("Colores preferidos", placeholder="ej: blanco y madera clara")
    objetivo = st.selectbox("Objetivo principal", ["Descansar", "Estudiar", "Trabajar", "Jugar", "Recibir gente"])
    enviado = st.form_submit_button("Generar recomendación")

if enviado:
    with st.spinner("Diseñando tu ambiente..."):
        recomendacion = generar_recomendacion(tipo_ambiente, dimensiones, estilo, presupuesto, colores, objetivo)

    st.subheader("Distribución")
    st.write(recomendacion.distribucion)

    st.subheader("Muebles sugeridos")
    st.write(recomendacion.muebles)

    st.subheader("Paleta de colores")
    st.write(recomendacion.paleta_colores)

    st.subheader("Iluminación")
    st.write(recomendacion.iluminacion)

    st.subheader("Materiales")
    st.write(recomendacion.materiales)

    st.subheader("Tips para optimizar el espacio")
    st.write(recomendacion.tips_espacio)

    st.subheader("Lista de elementos")
    st.write(recomendacion.lista_elementos)

with st.expander("ℹ️ Cómo funciona"):
    st.write(
        "Completá el formulario con las características de tu ambiente y apretá "
        "'Generar recomendación'. RoomCraft AI arma un prompt a partir de esos "
        "datos y se lo manda a una IA (Groq), que devuelve una propuesta de "
        "diseño organizada en distribución, muebles, colores, iluminación, "
        "materiales y más. Cada consulta tarda unos segundos."
    )
