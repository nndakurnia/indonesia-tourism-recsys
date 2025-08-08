import pandas as pd
import numpy as np
from app.core.config import DATA_PATH


def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.replace({np.nan: None})  # Ganti value NaN dengan None
    return df.to_dict(orient="records")
