import pandas as pd
import numpy as np
from config import DATE_COLUMN, SALES_COLUMN, FORECAST_DAYS
from sklearn.metrics import mean_absolute_error, mean_squared_error

def moving_average_forecast(df, window=3):
    """
    Forecast Model.
    """
    df = df.copy()
    df = df.set_index(DATE_COLUMN)
    df = df.asfreq("D") 
    df[SALES_COLUMN] = df[SALES_COLUMN].fillna(0)

    df["forecast"] = df[SALES_COLUMN].rolling(window=window).mean()

    last_date = df.index[-1]
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=FORECAST_DAYS)
    future_forecast = [df["forecast"].iloc[-1]] * FORECAST_DAYS  

    forecast_df = pd.DataFrame({DATE_COLUMN: future_dates, "forecast": future_forecast})
    return df.reset_index(), forecast_df


def evaluate_moving_average(df, window=3):
    """
    Evaluasi Moving Average dengan train-test split (80/20).
    """
    split_idx = int(len(df) * 0.8)
    train, test = df.iloc[:split_idx], df.iloc[split_idx:]

    # Forecast sederhana di train
    train = train.copy()
    train["forecast"] = train["jumlah_terjual"].rolling(window=window).mean()

    # Prediksi test = nilai forecast terakhir dari train
    last_forecast = train["forecast"].dropna().iloc[-1]
    test_forecast = [last_forecast] * len(test)

    # Hitung metrik
    mae = mean_absolute_error(test["jumlah_terjual"], test_forecast)
    rmse = np.sqrt(mean_squared_error(test["jumlah_terjual"], test_forecast))
    mape = np.mean(np.abs((test["jumlah_terjual"] - test_forecast) / test["jumlah_terjual"])) * 100

    return mae, rmse, mape

