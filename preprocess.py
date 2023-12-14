import numpy as np
import pandas as pd

df_path = '/home/davide/ai/Projects/GraphCluster/preprocessed_c.csv'

df = pd.read_csv(df_path)
numeric_columns = df.select_dtypes(include=['number']).columns
df_norm = df.copy()
for col in numeric_columns:
    series = df[col]
    mean = series.mean()
    std = series.std()
    
    series_norm = (series - mean) / std
    df_norm[col] = series_norm

df_path = '/home/davide/ai/Projects/GraphCluster/preprocessed_norm.csv'
df_norm.to_csv(df_path)