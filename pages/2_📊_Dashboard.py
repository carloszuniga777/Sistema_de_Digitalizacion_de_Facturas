import streamlit as st
from pathlib import Path
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from styles import aplicar_estilos

aplicar_estilos()


# ──────────────────── Configuración de página ─────────────────────────
st.set_page_config(
    page_title="Dashboard - Facturas",
    page_icon="📊",
    layout="wide"
)

# ──────────────────── Ruta de la Base de datos ────────────────────────
SQLITE_DB = Path(__file__).parent.parent / "src" / "database" / "facturas.db"

# ──────────────────── Estilos CSS ────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #fafbff 50%, #f5f0ff 100%);
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Header ── */
    .dash-header {
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }
    .dash-header-gastos {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 50%, #dc2626 100%);
        box-shadow: 0 8px 32px rgba(220, 38, 38, 0.25);
    }
    .dash-header-ingresos {
        background: linear-gradient(135deg, #157347 0%, #22c55e 50%, #157347 100%);
        box-shadow: 0 8px 32px rgba(21, 115, 71, 0.25);
    }
    .dash-header h1 {
        color: white;
        font-size: 1.7rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .dash-header p {
        color: rgba(255,255,255,0.8);
        font-size: 0.85rem;
        margin: 4px 0 0 0;
        font-weight: 300;
    }

    /* ── Tarjetas métricas ── */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(99, 102, 241, 0.1);
        text-align: center;
        height: 100%;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1f3a;
        font-family: 'DM Mono', monospace;
    }
    .metric-label {
        font-size: 0.72rem;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 4px;
    }
    .metric-icon {
        font-size: 1.4rem;
        margin-bottom: 8px;
    }

    /* ── Sección ── */
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06);
        border: 1px solid rgba(99, 102, 241, 0.08);
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 0.82rem;
        font-weight: 700;
        color: #6366f1;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 16px;
    }

    /* ── Filtros ── */
    .filter-bar {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid rgba(99, 102, 241, 0.08);
        margin-bottom: 20px;
    }

    /* ── Tabla ── */
    [data-testid="stDataFrame"] { border-radius: 10px; }

    /* ── Botones ── */
    .stButton > button {
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        border: 2px solid transparent !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }

    /* Botón descarga */
    [data-testid="stDownloadButton"] button {
        background: #ffc107 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        white-space: nowrap !important;
        width: auto !important;
    }
    [data-testid="stDownloadButton"] button:hover {
        background: #ffca2c !important;
        color: #000000 !important;
        border-color: #ffc720 !important;
    }


    /* ──────── Responsive ────── */
    
    @media (max-width: 768px) {
        .dash-header { padding: 18px 20px; }
        .dash-header h1 { font-size: 1.3rem; }
        .metric-value { font-size: 1.2rem; }
    }
    @media (max-width: 480px) {
        .dash-header h1 { font-size: 1.1rem; }
        .metric-value { font-size: 1rem; }
        .metric-card { padding: 14px 12px; }
    }

            
     /*Graficos de pastel*/              
    /* En pantallas medianas, apilar las columnas de los pies */
    @media (max-width: 768px) {
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
    [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {
        width: 100% !important;
        flex: none !important;
        min-width: 100% !important;
    }

   /*boton descarga*/                   
   @media (max-width: 768px) {
    [data-testid="stDownloadButton"] button {
        width: 100% !important;
    }
}         
}        
</style>
""", unsafe_allow_html=True)

# ──────────────────── Constantes ─────────────────────────────────────


MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

COLORES_GASTOS   = ["#dc2626", "#ef4444", "#f87171", "#fca5a5", "#fee2e2"]
COLORES_INGRESOS = ["#157347", "#22c55e", "#4ade80", "#86efac", "#bbf7d0"]


# ──────────────────── Cargar datos ───────────────────────────────────


with sqlite3.connect(SQLITE_DB) as conn:
    df = pd.read_sql("SELECT * FROM tbl_facturas", conn)

# Convierte a numerico
df["monto_total_lempiras"] = pd.to_numeric(df["monto_total_lempiras"], errors="coerce").fillna(0)
df["mes_factura"]          = pd.to_numeric(df["mes_factura"], errors="coerce")
df["ano_factura"]          = pd.to_numeric(df["ano_factura"], errors="coerce")

# ──────────────────── Filtros ────────────────────────────────────────

with st.container(border=True):
    col_tipo_factura, col_ano, _ = st.columns([1, 1, 2], gap="small")

    with col_tipo_factura:
        tipo_factura_selected = st.selectbox("🏷️ Tipo de Factura", options=["Gastos", "Ingresos"])             # Filtro de tipo de factura

    with col_ano:
        anos = sorted(df["ano_factura"].dropna().unique().astype(int).tolist(), reverse=True)
        ano_selected  = st.selectbox("📅 Año", options=["Todos"] + anos)                                       # Filtro de año




# ──────────────────── Aplicar filtros ────────────────────────────────

df_tipo_factura = df[df["tipo_factura"] == tipo_factura_selected].copy()                                 # Filtra por tipo de factura si es de gastos o ingresos

if ano_selected != "Todos":
    df_tipo_factura = df_tipo_factura[df_tipo_factura["ano_factura"] == int(ano_selected)]               # Filtra por ano


# ──────────────────── Colores según tipo ─────────────────────────────

es_gastos      = tipo_factura_selected == "Gastos"
color_primario = "#dc2626" if es_gastos else "#157347"
color_grad     = "dash-header-gastos" if es_gastos else "dash-header-ingresos"
colores_graf   = COLORES_GASTOS if es_gastos else COLORES_INGRESOS
icono          = "💸" if es_gastos else "💰"


# ──────────────────── Header ─────────────────────────────────────────
titulo    = "Gastos" if es_gastos else "Ingresos"
subtitulo = f"Resumen de {titulo.lower()} · {'Todos los años' if ano_selected == 'Todos' else str(ano_selected)}"

st.markdown(f"""
    <div class="dash-header {color_grad}">
        <div>
            <h1>{icono} Dashboard de {titulo}</h1>
            <p>{subtitulo}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# ──────────────────── Métricas ───────────────────────────────────────

total_facturas  = len(df_tipo_factura)                                            # Cantidad de facturas (Previamentes filtradas por factura y ano)  
monto_total     = df_tipo_factura["monto_total_lempiras"].sum()                   # Monto total de facturas (Previamentes filtradas por factura y ano)

# Datos de la tercera tarjeta se obtiene dinamicamente:
#   - Si es gastos obtiene la cantidad de provedores
#   - Si es ingresos obtiene la cantidad de clientes

if es_gastos:
    tercera_tarjeta_val   = df_tipo_factura["rtn_proveedor"].nunique()
    tercera_tarjeta_label = "Proveedores"
    tercera_tarjeta_icon  = "🏪"
else:
    tercera_tarjeta_val   = df_tipo_factura["rtn_cliente"].nunique() if "rtn_cliente" in df_tipo_factura.columns else 0
    tercera_tarjeta_label = "Clientes"
    tercera_tarjeta_icon  = "👥"


col1, col2, col3 = st.columns(3, gap="small")

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🧾</div>
            <div class="metric-value">{total_facturas}</div>
            <div class="metric-label">Total Facturas</div>
        </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icono}</div>
            <div class="metric-value">L. {monto_total:,.0f}</div>
            <div class="metric-label">Monto Total</div>
        </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{tercera_tarjeta_icon}</div>
            <div class="metric-value">{tercera_tarjeta_val}</div>
            <div class="metric-label">{tercera_tarjeta_label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────── Gráfico de barras por mes ──────────────────────

with st.container(border=True):
    st.markdown(f'<div class="section-title">📅 {titulo} por mes</div>', unsafe_allow_html=True)

    # Crear DataFrame con todos los meses del año
    todos_meses = pd.DataFrame({
        "mes_num":  list(MESES.keys()),
        "mes_nombre": list(MESES.values())
    })

    # Si Dataframe tiene filas y mes_factura no es null/NaN
    if not df_tipo_factura.empty and df_tipo_factura["mes_factura"].notna().any():
        df_meses = df_tipo_factura.groupby("mes_factura")["monto_total_lempiras"].sum().reset_index()              # Se obtiene el total de montos agrupados por meses
        df_meses.columns = ["mes_num", "monto"]                                                                    # Nombra las columnas 
        df_meses = todos_meses.merge(df_meses, on="mes_num", how="left").fillna(0)                                 # Une los meses del ano con los montos, para obtener el nombre del mes y su respectivo monto
    else:
        df_meses = todos_meses.copy()
        df_meses["monto"] = 0


    # Grafico de barras
    fig_barras = go.Figure(go.Bar(
        x=df_meses["mes_nombre"],
        y=df_meses["monto"],
        marker_color=color_primario,
        marker_line_width=0,
        text=[f"L. {v:,.0f}" if v > 0 else "" for v in df_meses["monto"]],
        textposition="outside",
        textfont=dict(size=10, family="DM Sans"),
    ))


    fig_barras.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="DM Sans", size=12, color="#8892b0"),
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f1f5f9",
            tickformat=",.0f",
            tickprefix="L. ",
        ),
        margin=dict(t=20, b=10, l=10, r=10),
        height=320,
        showlegend=False,
    )

    st.plotly_chart(fig_barras, use_container_width=True)




# ──────────────────── Gráficos de pastel ─────────────────────────────
if es_gastos:
    col_pie1, col_pie2 = st.columns(2, gap="small")

    # Pie 1: Top 5 proveedores
    with col_pie1:
        with st.container(border=True):
            st.markdown('<div class="section-title">🏪 Top 5 Proveedores</div>', unsafe_allow_html=True)

            df_prov = (
                df_tipo_factura.groupby("proveedor")["monto_total_lempiras"]
                .sum().reset_index()
                .sort_values("monto_total_lempiras", ascending=False)
                .head(5)
            )

            #Si hay informacion grafica
            if not df_prov.empty:
                fig_prov = px.pie(
                    df_prov,
                    names="proveedor",
                    values="monto_total_lempiras",
                    color_discrete_sequence=COLORES_GASTOS,
                    hole=0.4,
                )
                fig_prov.update_traces(
                    textposition="inside",
                    textinfo="percent",
                    textfont_size=11,
                    hovertemplate="<b>%{label}</b><br>L. %{value:,.0f}<br>%{percent}<extra></extra>",
                )
                fig_prov.update_layout(
                    paper_bgcolor="white",
                    font=dict(family="DM Sans"),
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=300,
                    showlegend=True,
                    legend=dict(font=dict(size=10)),
                )
                st.plotly_chart(fig_prov, use_container_width=True)
            else:
                st.info("Sin datos disponibles")


    # Pie 2: Top 5 categorías
    with col_pie2:
        with st.container(border=True):
            st.markdown('<div class="section-title">🏷️ Top 5 Categorías</div>', unsafe_allow_html=True)

            df_cat = (
                df_tipo_factura.groupby("categoria")["monto_total_lempiras"]
                .sum().reset_index()
                .sort_values("monto_total_lempiras", ascending=False)
                .head(5)
            )

            if not df_cat.empty:
                fig_cat = px.pie(
                    df_cat,
                    names="categoria",
                    values="monto_total_lempiras",
                    color_discrete_sequence=["#f97316", "#fb923c", "#fdba74", "#fed7aa", "#ffedd5"],
                    hole=0.4,
                )
                fig_cat.update_traces(
                    textposition="inside",
                    textinfo="percent",
                    textfont_size=11,
                    hovertemplate="<b>%{label}</b><br>L. %{value:,.0f}<br>%{percent}<extra></extra>",
                )
                fig_cat.update_layout(
                    paper_bgcolor="white",
                    font=dict(family="DM Sans"),
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=300,
                    showlegend=True,
                    legend=dict(font=dict(size=10)),
                )
                st.plotly_chart(fig_cat, use_container_width=True)
            else:
                st.info("Sin datos disponibles")


else:
    # Pie: Top 5 clientes
    
    with st.container(border=True):
        st.markdown('<div class="section-title">👥 Top 5 Clientes</div>', unsafe_allow_html=True)

        df_cli = (
            df_tipo_factura.groupby("nombre_cliente")["monto_total_lempiras"]
            .sum().reset_index()
            .sort_values("monto_total_lempiras", ascending=False)
            .head(5)
        )

        # Si hay informacion grafica
        if not df_cli.empty:
            fig_cli = px.pie(
                df_cli,
                names="nombre_cliente",
                values="monto_total_lempiras",
                color_discrete_sequence=COLORES_INGRESOS,
                hole=0.4,
            )
            fig_cli.update_traces(
                textposition="inside",
                textinfo="percent",
                textfont_size=11,
                hovertemplate="<b>%{label}</b><br>L. %{value:,.0f}<br>%{percent}<extra></extra>",
            )
            fig_cli.update_layout(
                paper_bgcolor="white",
                font=dict(family="DM Sans"),
                margin=dict(t=10, b=10, l=10, r=10),
                height=320,
                showlegend=True,
                legend=dict(font=dict(size=11)),
            )
            st.plotly_chart(fig_cli, use_container_width=True)
        else:
            st.info("Sin datos disponibles")





# ──────────────────── Tabla resumen ──────────────────────────────────

with st.container(border=True):

    col_titulo, col_descarga = st.columns([3, 1])

    with col_titulo:
         st.markdown(f'<div class="section-title">📋 Tabla de {titulo}</div>', unsafe_allow_html=True)


    #-------------- Boton descarga excel -----------------
    with col_descarga:
        
        # Filtro ano seleccionado
        # Obtener todas las facturas del año seleccionado (sin filtro de tipo)
        if ano_selected != "Todos":
            df_descarga = df[df["ano_factura"] == int(ano_selected)]
        else:
            df_descarga = df.copy()

       
        columnas_exportar = [
            "fecha_factura",
            "numero_factura",
            "rtn_proveedor",
            "proveedor",
            "rtn_cliente",
            "nombre_cliente",
            "concepto",
            "monto_total",
            "moneda",
            "monto_total_lempiras",
            "tipo_factura",
            "categoria",
        ]


        columnas_validas = [c for c in columnas_exportar if c in df_descarga.columns]
        df_descarga = df_descarga[columnas_validas].copy()

        # Tipos de datos para que Excel los reconozca automáticamente
        df_descarga["fecha_factura"]        = pd.to_datetime(df_descarga["fecha_factura"], errors="coerce").dt.strftime("%Y-%m-%d")
        df_descarga["monto_total"]          = pd.to_numeric(df_descarga["monto_total"],          errors="coerce")
        df_descarga["monto_total_lempiras"] = pd.to_numeric(df_descarga["monto_total_lempiras"], errors="coerce")

        # Agrega apóstrofe al inicio para que excel no borre los 0 al inicio
        df_descarga["rtn_proveedor"]  = "'" + df_descarga["rtn_proveedor"].astype(str).fillna("")
        df_descarga["rtn_cliente"]  = "'" + df_descarga["rtn_cliente"].astype(str).fillna("")
        df_descarga["numero_factura"] = "'" + df_descarga["numero_factura"].astype(str).fillna("")


        # Exportar a Excel
        csv = df_descarga.to_csv(index=False, encoding="utf-8-sig")

        # Botón de descarga
        st.download_button(
            label=f"⬇️ Descargar {ano_selected if ano_selected != 'Todos' else 'todas las facturas'}",
            data=csv,
            file_name=f"facturas_{ano_selected}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    #-----------------------------------------------------

   

    columnas_mostrar = [
        "fecha_factura", "numero_factura", "proveedor",
        "nombre_cliente", "rtn_cliente", "concepto", "monto_total_lempiras",
        "moneda", "tipo_factura", "categoria"
    ]

    columnas_validas = [c for c in columnas_mostrar if c in df_tipo_factura.columns]


    st.dataframe(
        df_tipo_factura[columnas_validas],
        use_container_width=True,
        hide_index=True,
        column_config={
            "fecha_factura":        st.column_config.TextColumn("Fecha"),
            "numero_factura":       st.column_config.TextColumn("N° Factura"),
            "rtn_proveedor":        st.column_config.TextColumn("RTN Proveedor", width="medium"),
            "proveedor":            st.column_config.TextColumn("Proveedor"),
            "rtn_cliente":          st.column_config.TextColumn("RTN Cliente",   width="medium"),
            "nombre_cliente":       st.column_config.TextColumn("Cliente"),
            "concepto":             st.column_config.TextColumn("Concepto"),
            "monto_total_lempiras": st.column_config.NumberColumn("Monto (L)", format="L. %.2f"),
            "tipo_factura":         st.column_config.TextColumn("Tipo"),
            "categoria":            st.column_config.TextColumn("Categoría"),
        }
    )



