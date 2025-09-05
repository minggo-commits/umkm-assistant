import pandas as pd
from config import DATE_COLUMN, PRODUCT_COLUMN, SALES_COLUMN

def preprocess_data(df):
    required_cols = [DATE_COLUMN, PRODUCT_COLUMN, SALES_COLUMN]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Dataset harus mengandung kolom: {required_cols}")

    # Konversi tanggal
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")
    df = df.dropna(subset=[DATE_COLUMN])

    # Mengurutkan data
    df = df.sort_values(by=DATE_COLUMN)
    return df
