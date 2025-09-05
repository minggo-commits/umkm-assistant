import pandas as pd

def load_data(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    elif file.name.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file)
    else:
        raise ValueError("Format file tidak didukung. Gunakan CSV atau Excel.")
    return df
