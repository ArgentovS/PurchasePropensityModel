import pandas as pd


# Проставим к каждому товару наиболее часто встречающееся значение цвета
# в мультипроцессорном режиме
def freq_product_color(product, df):
    print(product, end="  |  ")
    try:
        top = df[df["product"] == product].describe()["colour"]["top"]
        print(top)
        return top
    except:
        return None


def add_freq_product_color(dft):
    df_unique = dft[0]
    df = dft[1]
    df_unique["freq_color"] = df_unique["product"].apply(
        lambda x: freq_product_color(x, df)
    )
    return df_unique
