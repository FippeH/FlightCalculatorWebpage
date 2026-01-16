import streamlit as st
from calculations import *
from weather import hämta_MET_TAF

st.set_page_config(
    page_title="Flygberäkningsverktyg -- Haverinen",
    page_icon="icon.png",
    layout="wide"
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1.5rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        max-width: 900px;
        margin: auto;
    }
    button[kind="primary"] {
        width: 100%;
    }
    </style>

    <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
    """,
    unsafe_allow_html=True,
)

st.title("✈️ Flygberäkningsverktyg")

val = st.selectbox(
    "Välj funktion",
    [
        "True Airspeed",
        "Vindupphållningsvinkel",
        "Markhastighet",
        "Tryckhöjd",
        "Densitetshöjd",
        "Vindkomposant",
        "Radioräckvidd",
        "Blocktid",
        "METAR / TAF",
    ],
)

st.divider()

def center_block():
    left, center, right = st.columns([0.1, 0.8, 0.1])
    return center

# --- TAS ---
if val == "True Airspeed":
    c = center_block()
    with c:
        st.subheader("True Airspeed")
        alt = st.number_input("Höjd (ft)", value=2000, step=100)
        ias = st.number_input("IAS (kt)", value=100, step=1)
        qnh = st.number_input("QNH (hPa)", value=1013, step=1)
        oat = st.number_input("Temperatur (°C)", value=10, step=1)
        if st.button("Beräkna TAS"):
            st.success(f"TAS: {beräkna_TAS(alt, ias, qnh, oat)}")

elif val == "Vindupphållningsvinkel":
    c = center_block()
    with c:
        st.subheader("Vindupphållningsvinkel")
        ws = st.number_input("Vindhastighet (kt)", value=10, step=1)
        tas = st.number_input("True Airspeed (kt)", value=100, step=1)
        wd = st.number_input("Vindriktning (°)", value=180, step=1)
        mt = st.number_input("Magnetisk track (°)", value=90, step=1)
        if st.button("Beräkna WCA"):
            st.success(beräkna_WCA(ws, tas, wd, mt))

elif val == "Markhastighet":
    c = center_block()
    with c:
        st.subheader("Markhastighet")
        tas = st.number_input("True Airspeed (kt)", value=100, step=1)
        ws = st.number_input("Vindhastighet (kt)", value=10, step=1)
        wd = st.number_input("Vindriktning (°)", value=180, step=1)
        mh = st.number_input("Magnetisk kurs (°)", value=90, step=1)
        if st.button("Beräkna GS"):
            st.success(f"GS: {beräkna_GS(tas, ws, wd, mh)}")

elif val == "Tryckhöjd":
    c = center_block()
    with c:
        st.subheader("Tryckhöjd")
        alt = st.number_input("Platsens höjd (ft)", value=200, step=50)
        qnh = st.number_input("QNH (hPa)", value=1013, step=1)
        if st.button("Beräkna tryckhöjd"):
            st.success(f"Tryckhöjd: {beräkna_TH(alt, qnh)}")

elif val == "Densitetshöjd":
    c = center_block()
    with c:
        st.subheader("Densitetshöjd")
        alt = st.number_input("Platsens höjd (ft)", value=200, step=50)
        qnh = st.number_input("QNH (hPa)", value=1013, step=1)
        oat = st.number_input("Temperatur (°C)", value=10, step=1)
        if st.button("Beräkna densitetshöjd"):
            st.success(f"Densitetshöjd: {beräkna_DH(alt, qnh, oat)}")

elif val == "Vindkomposant":
    c = center_block()
    with c:
        st.subheader("Vindkomposant")
        rw = st.number_input("Banriktning (°)", value=90, step=1)
        wd = st.number_input("Vindriktning (°)", value=180, step=1)
        ws = st.number_input("Vindhastighet (kt)", value=10, step=1)
        if st.button("Beräkna vindkomposant"):
            st.success(beräkna_VK(rw, wd, ws))

elif val == "Radioräckvidd":
    c = center_block()
    with c:
        st.subheader("Radioräckvidd")
        alt = st.number_input("Flygplanets höjd (ft)", value=2000, step=100)
        gnd = st.number_input("Stationens höjd (ft)", value=200, step=50)
        if st.button("Beräkna radioräckvidd"):
            st.success(f"Räckvidd: {beräkna_RR(alt, gnd)}")

elif val == "Blocktid":
    c = center_block()
    with c:
        st.subheader("Blocktid")
        onb = st.text_input("ON-BLOCK (HHMM)", value="1030")
        offb = st.text_input("OFF-BLOCK (HHMM)", value="1215")
        if st.button("Beräkna blocktid"):
            st.success(beräkna_BT(onb, offb))

elif val == "METAR / TAF":
    c = center_block()
    with c:
        st.subheader("METAR / TAF")
        icao = st.text_input("ICAO-kod", value="ESGG").upper()
        if st.button("Hämta METAR/TAF"):
            text = hämta_MET_TAF(icao)
            st.code(text)
