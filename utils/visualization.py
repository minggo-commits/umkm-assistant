import matplotlib.pyplot as plt
from config import DATE_COLUMN, SALES_COLUMN

def plot_forecast(history_df, forecast_df):
    plt.figure(figsize=(10,5))
    plt.plot(history_df[DATE_COLUMN], history_df[SALES_COLUMN], label="Historis", marker="o")
    if "forecast" in history_df.columns:
        plt.plot(history_df[DATE_COLUMN], history_df["forecast"], label="Moving Average", linestyle="--")
    plt.plot(forecast_df[DATE_COLUMN], forecast_df["forecast"], label="Prediksi", marker="x")
    plt.xlabel("Tanggal")
    plt.ylabel("Jumlah Terjual")
    plt.title("Forecasting Penjualan Produk")
    plt.legend()
    plt.grid(True)
    return plt
