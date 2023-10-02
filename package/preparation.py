import pandas as pd
import os


# Проставим к каждому товару наиболее часто встречающееся значение цвета
# в мультипроцессорном режиме
def freq_product_color(product: str, df: pd.DataFrame):
    a = df[df["product"] == product].describe()["colour"]["top"]
    return a


def add_freq_product_color(dft):
    df_unique: pd.DataFrame = dft[0]
    df: pd.DataFrame = dft[1]
    df_unique["freq_color"] = df_unique["product"].apply(
        lambda x: freq_product_color(x, df)
    )
    return df_unique
