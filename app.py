import streamlit as st
import requests
import time

st.set_page_config(
    page_title="Rastreador Soul-Link 4P",
    page_icon="⚔️",
    layout="wide"
)

# Conexión protegida mediante Secrets
FIREBASE_URL = st.secrets["FIREBASE_URL"]
JUGADORES = ["abraham", "ruben", "jona", "juan"]

# ==========================================================
# MAPEO COMPLETO DE UBICACIONES (POKÉMON UNBOUND / CFRU)
# ==========================================================
MAPAS_UNBOUND = {
    # Prólogo y zonas iniciales
    "0xC5": "Frozen Heights (Inicial)",
    "0xC6": "Ruta 1",
    "0xC7": "Bell Pet Factory",
    "0xC8": "Bellboyant",
    "0xC9": "Dresco Town",
    "0xCA": "Ruta 2",
    "0xCB": "Grimwood Forest",
    "0xCC": "Fallshore City",
    "0xCD": "Ruta 3",
    "0xCE": "Cinder Volcano",
    "0xCF": "Ruta 4",
    "0xD0": "Tehl Town",
    "0xD1": "Ruta 5",
    "0xD2": "Valley Cave",
    "0xD3": "Crater Town",
    "0xD4": "Ruta 6",
    "0xD5": "Ruta 7",
    "0xD6": "Frost Mountain",
    "0xD7": "Blizzard City",
    "0xD8": "Ruta 8",
    "0xD9": "Frozen Forest",
    "0xDA": "Ruta 9",
    "0xDB": "Tomb of Borrius",
    "0xDC": "Dehara City",
    "0xDD": "Ruta 10",
    "0xDE": "ThunderCap Mountain",
    "0xDF": "Ruta 11",
    "0xE0": "Ruta 12",
    "0xE1": "Vivill Town",
    "0xE2": "Ruta 13",
    "0xE3": "Ruta 14",
    "0xE4": "Tarsabon City",
    "0xE5": "Ruta 15",
    "0xE6": "Antisis City",
    "0xE7": "Ruta 16",
    "0xE8": "Ruta 17",
    "0xE9": "Seaport City",
    "0xEA": "Ruta 18",
    "0xEB": "Victory Road",
    "0xEC": "Pokémon League",
    "0xED": "Cube Corp.",
    "0xEE": "Magnolia Town",
    "0xEF": "Redwood Village",
    "0xF0": "Redwood Forest",
    "0xFE": "Regalo / Evento Especial",
    "0xFF": "Intercambio / Desconocido",
    # Mapeos clásicos heredados de base FireRed
    "0x00": "Pueblo Paleta",
    "0x01": "Ciudad Viridian",
    "0x02": "Ciudad Pewter",
    "0x03": "Ciudad Cerulean",
    "0x04": "Ciudad Lavender",
    "0x05": "Ciudad Vermilion",
    "0x06": "Ciudad Celadon",
    "0x07": "Ciudad Fucsia",
    "0x08": "Ciudad Azafrán",
    "0x09": "Isla Canela",
    "0x58": "Zona Safari"
}

def traducir_ubicacion(ruta_str):
    if not ruta_str:
        return "Desconocida"
    
    # Extraer el valor hex si viene con formato 'Ruta_0x...'
    clave_hex = ruta_str.replace("Ruta_", "").strip()
    
    # Buscar coincidencia exacta
    if clave_hex in MAPAS_UNBOUND:
        return MAPAS_UNBOUND[clave_hex]
    if ruta_str in MAPAS_UNBOUND:
        return MAPAS_UNBOUND[ruta_str]
        
    return ruta_str.replace("_", " ")

def obtener_datos_jugador(nombre):
    try:
        url = f"{FIREBASE_URL}/jugadores/{nombre}.json"
        r = requests.get(url, timeout=3)
        if r.status_code == 200 and r.json():
            data = r.json()
            if isinstance(data, dict) and "equipo" in data:
                return data["equipo"]
            elif isinstance(data, list):
                return data
        return []
    except Exception:
        return []

def obtener_rutas_caidas():
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

# Cabecera
st.title("⚔️ Pokémon Desatado: Cuádruple de Vínculo de Alma")

# Sección Deathlink
st.subheader("💀 Rutas Caídas (Deathlink)")
rutas_caidas = obtener_rutas_caidas()

if rutas_caidas:
    rutas_limpias = [traducir_ubicacion(r) for r in rutas_caidas]
    st.error(f"**Rutas bloqueadas para todos:** {', '.join(rutas_limpias)}")
else:
    st.success("¡No hay bajas registradas todavía! Todas las rutas siguen disponibles.")

st.markdown("---")

# Columnas de los 4 jugadores
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
                ruta_cruda = poke.get("ruta", "Desconocida")
                
                # Traducir el código hex a nombre legible de Unbound
                ruta = traducir_ubicacion(ruta_cruda)

                porcentaje = 0.0
                if hp_max > 0:
                    porcentaje = min(max(hp_actual / hp_max, 0.0), 1.0)

                with st.container(border=True):
                    st.markdown(f"**{nombre}** ({estado})")
                    st.caption(f"📍 {ruta}")
                    st.progress(porcentaje, text=f"HP: {hp_actual} / {hp_max}")

time.sleep(3)
st.rerun()
