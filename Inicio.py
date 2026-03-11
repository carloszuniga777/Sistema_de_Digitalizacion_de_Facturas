# Configuracion inicial de paginas

import streamlit as st

st.set_page_config(
    page_title="Sistema de Facturas",
    page_icon="🧾",
    layout="wide"
)

st.switch_page("pages/1_📋_Facturas.py")