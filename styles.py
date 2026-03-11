import streamlit as st

def aplicar_estilos():
    st.markdown("""
    <style>
        /* todos tus estilos CSS aquí */
        
        [data-testid="stExpandSidebarButton"] {
            visibility: visible !important;
            display: flex !important;
            opacity: 1 !important;
            position: fixed !important;
            top: 14px !important;
            left: 14px !important;
            z-index: 999999 !important;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
                

           /* Scrollbar bonito */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 3px; }
        ::-webkit-scrollbar-thumb { background: #c7d2fe; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #6366f1; }        
    
    </style>
    """, unsafe_allow_html=True)