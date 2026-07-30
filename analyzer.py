import pandas as pd

def load_dataset(path):
    if path.endswith(".csv"):
        return pd.read_csv(path)

    if path.endswith(".xlsx"):
        return pd.read_excel(path)

    if path.endswith(".xls"):
        return pd.read_excel(path)

    raise Exception("Unsupported file format")