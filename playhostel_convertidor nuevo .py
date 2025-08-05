
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="PlayHostel Convertidor", layout="centered")

st.markdown("""
<style>
    html, body, [class*="css"]  {
        background-color: #1d5a66;
        color: #fffdf7;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stButton>button {
        background-color: #b9442c;
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
    .stFileUploader {
        background-color: #f8ebd8;
        padding: 1.5rem;
        border-radius: 12px;
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

st.image("playhostel_convertidor_mockup.png", use_column_width=True)
st.title("PlayHostel Convertidor")
st.caption("Diseñada y programada por Jaime F. Paleo")

uploaded_file = st.file_uploader("Subí tu archivo (Excel, PDF, CSV, etc.)", type=["csv", "xls", "xlsx", "pdf", "txt"])

def es_formato_frontdesk(df):
    columnas_frontdesk = ["N°", "Nombre", "Apellido", "DNI", "Nacionalidad", "Fecha de ingreso", "Fecha de egreso"]
    return all(col in df.columns for col in columnas_frontdesk)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            st.warning("⚠️ Formato de archivo no soportado todavía.")
            st.stop()

        if es_formato_frontdesk(df):
            st.error("⚠️ Este archivo ya tiene formato FrontDesk. No se puede usar como fuente de datos.")
        else:
            st.success("✅ Archivo cargado correctamente. Generando archivo compatible...")

            columnas_salida = ["N°", "Nombre", "Apellido", "DNI", "Nacionalidad", "Fecha de ingreso", "Fecha de egreso"]
            df_salida = pd.DataFrame(columns=columnas_salida)

            for i in range(len(df)):
                fila = df.iloc[i]
                df_salida.loc[i] = [
                    i + 1,
                    fila.get("Nombre", ""),
                    fila.get("Apellido", ""),
                    fila.get("DNI", ""),
                    fila.get("Nacionalidad", ""),
                    fila.get("Fecha de ingreso", ""),
                    fila.get("Fecha de egreso", "")
                ]

            buffer = io.BytesIO()
            df_salida.to_excel(buffer, index=False, engine='openpyxl')
            st.download_button("📥 Convertir y descargar", buffer.getvalue(), file_name="huespedes_frontdesk.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
