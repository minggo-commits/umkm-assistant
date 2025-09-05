import pandas as pd
from config import DATE_COLUMN, SALES_COLUMN, FORECAST_DAYS

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
