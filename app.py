import streamlit as st
import requests
import time

# Configuración visual de la página
st.set_page_config(
    page_title="Rastreador Soul-Link 4P",
    page_icon="⚔️",
    layout="wide"
)

# Conexión protegida mediante Secrets
FIREBASE_URL = st.secrets["FIREBASE_URL"]

JUGADORES = ["abraham", "ruben", "jona", "juan"]

def obtener_datos_jugador(nombre):
    """Consulta los datos de cada jugador en Firebase Realtime Database."""
    try:
        url = f"{FIREBASE_URL}/jugadores/{nombre}.json"
        r = requests.get(url, timeout=3)
        if r.status_code == 200 and r.json():
            data = r.json()
            # Si viene empaquetado dentro de la clave 'equipo'
            if isinstance(data, dict) and "equipo" in data:
                return data["equipo"]
            # Si viene directamente como lista
            elif isinstance(data, list):
                return data
        return []
    except Exception:
        return []

def obtener_rutas_caidas():
    """Consulta la lista global de rutas caídas por Deathlink."""
    try:
        url = f"{FIREBASE_URL}/rutas_caidas.json"
        r = requests.get(url, timeout=3)
        if r.status_code == 200 and r.json():
            data = r.json()
            if isinstance(data, dict):
                return list(data.keys())
            elif isinstance(data, list):
                return [x for x in data if x]
        return []
    except Exception:
        return []

# Título principal
st.title("⚔️ Pokémon Desatado: Cuádruple de Vínculo de Alma")

# Sección de Rutas Caídas (Deathlink)
st.subheader("💀 Rutas Caídas (Deathlink)")
rutas_caidas = obtener_rutas_caidas()

if rutas_caidas:
    st.error(f"**Rutas bloqueadas para todo el equipo:** {', '.join(rutas_caidas)}")
else:
    st.success("¡No hay bajas registradas todavía! Todas las rutas siguen disponibles.")

st.markdown("---")

# Tablero de columnas para los 4 jugadores
cols = st.columns(4)

for i, jugador in enumerate(JUGADORES):
    with cols[i]:
        st.subheader(jugador.capitalize())
        equipo = obtener_datos_jugador(jugador)

        if not equipo:
            st.warning("Sin datos / Desconectado")
        else:
            for poke in equipo:
                nombre = poke.get("nombre", "Desconocido")
                hp_actual = poke.get("hp_actual", 0)
                hp_max = poke.get("hp_max", 1)
                estado = poke.get("estado", "Vivo")
                ruta = poke.get("ruta", "Ruta desconocida")

                porcentaje = 0.0
                if hp_max > 0:
                    porcentaje = min(max(hp_actual / hp_max, 0.0), 1.0)

                # Tarjeta individual para cada Pokémon
                with st.container(border=True):
                    st.markdown(f"**{nombre}** ({estado})")
                    st.caption(f"📍 {ruta}")
                    st.progress(porcentaje, text=f"HP: {hp_actual} / {hp_max}")

# Pausa breve antes de refrescar automáticamente
time.sleep(3)
st.rerun()
