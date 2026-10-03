import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Soul-Link 4P Tracker", layout="wide", page_icon="🔗")

st.title("⚔️ Pokémon Unbound: Soul-Link Cuádruple")

# Reemplaza con tu URL real de Firebase
FIREBASE_URL = st.secrets["FIREBASE_URL"]

# Los 4 integrantes
JUGADORES = ["abraham", "ruben", "jona", "juan"]

def cargar_datos_jugador(jugador):
    try:
        r = requests.get(f"{FIREBASE_URL}/jugadores/{jugador}.json", timeout=2)
        datos = r.json()
        if isinstance(datos, list):
            return datos
        return []
    except Exception:
        return []

def cargar_muertes_globales():
    try:
        r = requests.get(f"{FIREBASE_URL}/muertes.json", timeout=2)
        datos = r.json()
        if isinstance(datos, dict):
            return datos
        return {}
    except Exception:
        return {}

# 1. Resumen de Bajas Globales (Deathlink)
muertes = cargar_muertes_globales()
if muertes:
    st.subheader("💀 Rutas Caídas (Deathlink)")
    rutas_muertas = []
    for r, meta in muertes.items():
        if isinstance(meta, dict):
            autor = meta.get('autor', 'Desconocido')
        else:
            autor = str(meta)
        rutas_muertas.append(f"**{r}** (por {autor})")
    st.error(" | ".join(rutas_muertas))
st.divider()

# 2. Columnas en vivo para cada jugador
columnas = st.columns(4)

for i, jugador in enumerate(JUGADORES):
    with columnas[i]:
        st.subheader(jugador.capitalize())
        datos = cargar_datos_jugador(jugador)

        if not datos:
            st.warning("Sin datos / Desconectado")
            continue

        equipo = []
        fallos = []

        for item in datos:
            if not isinstance(item, dict):
                continue
            if item.get("tipo") == "fallo":
                fallos.append(item.get("ruta", ""))
            elif item.get("tipo") == "pokemon":
                equipo.append({
                    "Pokémon": item.get("nombre", "Desconocido"),
                    "PS": item.get("hp", "0/0"),
                    "Estado": "❤️ Vivo" if item.get("estado") == "Vivo" else "💀 Fainted",
                    "Ruta": item.get("origen", "Desconocido")
                })

        if equipo:
            df = pd.DataFrame(equipo)
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.info("Equipo vacío")

        if fallos:
            st.caption(f"🚫 **Fallos:** {', '.join(fallos)}")

# Refresco automático cada 3 segundos
time.sleep(3)
st.rerun()
