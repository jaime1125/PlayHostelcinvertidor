
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="PlayHostel Convertidor", layout="centered")

st.title("PlayHostel Convertidor")
st.caption("Diseñada y programada por Jaime F. Paleo, con ayuda de ChatGPT")

uploaded_file = st.file_uploader("Subí tu archivo (Excel, PDF, CSV, etc.)", type=["csv", "xls", "xlsx", "pdf", "txt"])

def es_formato_frontdesk(df):
    columnas_frontdesk = ["N°", "Nombre", "Apellido", "DNI", "Nacionalidad", "Fecha de ingreso", "Fecha de egreso"]
    return all(col in df.columns for col in columnas_frontdesk)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
            df = pd.read_excel(uploaded_file)
        else:
            st.warning("Formato de archivo no soportado todavía.")
            st.stop()

        if es_formato_frontdesk(df):
            st.error("⚠️ Este archivo ya tiene formato FrontDesk. No se puede usar como fuente de datos.")
        else:
            st.success("Archivo cargado correctamente. Generando archivo compatible...")

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
            st.download_button("📥 Descargar archivo compatible", buffer.getvalue(), file_name="huespedes_frontdesk.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
