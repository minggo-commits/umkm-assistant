import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from models.forecasting import moving_average_forecast
from utils.visualization import plot_forecast
from config import PRODUCT_COLUMN, SALES_COLUMN, DATE_COLUMN
from models.forecasting import evaluate_moving_average

st.set_page_config(page_title="UMKM Demand Forecasting", layout="wide")

st.title("📈 UMKM Demand Forecasting (MVP)")
st.write("Upload data penjualan (CSV/Excel) untuk mendapatkan prediksi permintaan produk.")

# Upload file
file = st.file_uploader("Upload file penjualan (CSV/Excel)", type=["csv", "xls", "xlsx"])

if file is not None:
    try:
        df = load_data(file)
        df = preprocess_data(df)

        # Pilih produk
        products = df[PRODUCT_COLUMN].unique()
        selected_product = st.selectbox("Pilih produk", products)

        product_df = df[df[PRODUCT_COLUMN] == selected_product]

        # Forecast
        history_df, forecast_df = moving_average_forecast(product_df)

        # Visualisasi
        st.subheader(f"Prediksi Penjualan: {selected_product}")
        st.pyplot(plot_forecast(history_df, forecast_df))

        # Rekomendasi stok
        recommended_stock = int(forecast_df["forecast"].sum())
        st.success(f"👉 Rekomendasi stok {selected_product} untuk 7 hari ke depan: **{recommended_stock} unit**")

        # Tabel hasil prediksi
        st.subheader("Detail Prediksi Harian")
        st.dataframe(forecast_df)

        # Evaluasi model
        mae, rmse, mape = evaluate_moving_average(product_df)

        st.subheader("📊 Evaluasi Model (Moving Average)")
        st.write(f"- MAE  : {mae:.2f}")
        st.write(f"- RMSE : {rmse:.2f}")
        st.write(f"- MAPE : {mape:.2f}%")


    except Exception as e:
        st.error(f"Terjadi error: {e}")
