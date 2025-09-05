import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from utils.data_loader import load_data
from utils.preprocessing import preprocess_data
from models.forecasting import moving_average_forecast
from utils.visualization import plot_forecast
from config import PRODUCT_COLUMN, SALES_COLUMN, DATE_COLUMN
from models.forecasting import evaluate_moving_average

def show_sales_insights(df):
            st.header("📊 Sales Insights Dashboard")

            # 1. Produk terlaris
            st.subheader("Top Produk Terlaris")
            top_products = df.groupby("produk")["jumlah_terjual"].sum().sort_values(ascending=False)
            st.bar_chart(top_products)

            # 2. Tren penjualan harian
            st.subheader("Tren Penjualan Harian")
            daily_sales = df.groupby("tanggal")["jumlah_terjual"].sum()
            st.line_chart(daily_sales)

            # 3. Hari paling ramai
            st.subheader("Hari Paling Ramai (Rata-rata Penjualan)")
            df["day_name"] = df["tanggal"].dt.day_name()
            avg_by_day = df.groupby("day_name")["jumlah_terjual"].mean()
            avg_by_day = avg_by_day.reindex(
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            )
            fig, ax = plt.subplots()
            sns.barplot(x=avg_by_day.index, y=avg_by_day.values, ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # 4. Ringkasan statistik
            st.subheader("Ringkasan Statistik")
            total_sales = df["jumlah_terjual"].sum()
            best_product = top_products.index[0]
            best_product_sales = top_products.iloc[0]
            avg_sales_per_day = daily_sales.mean()

            st.write(f"- Total penjualan: **{total_sales} unit**")
            st.write(f"- Produk terlaris: **{best_product} ({best_product_sales} unit)**")
            st.write(f"- Rata-rata penjualan per hari: **{avg_sales_per_day:.2f} unit**")


st.set_page_config(page_title="UMKM Demand Forecasting", layout="wide")

st.title("📈 UMKM Demand Forecasting (MVP)")
st.write("Upload data penjualan (CSV/Excel) untuk mendapatkan prediksi permintaan produk.")

# Upload file
file = st.file_uploader("Upload file penjualan (CSV/Excel)", type=["csv", "xls", "xlsx"])

df = None
if file is not None:
    try:
        df = load_data(file)
        df = preprocess_data(df)
    except Exception as e:
        st.error(f"Terjadi eror saat membaca data: {e}")

tab1, tab2 = st.tabs(["🔮 Forecasting", "📊 Sales Insights"])

with tab1:
    if df is not None:
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

with tab2:
    if df is not None:
        show_sales_insights(df)
    else:
        st.info("Silahkan upload dataset terlebih dahulu")
    