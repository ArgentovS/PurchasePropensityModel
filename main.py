import multiprocessing
from multiprocessing import Pool, Manager
import datetime as dt
from package.preparation import add_freq_product_color, freq_product_color

import pandas as pd

df_non_colours = pd.DataFrame({"a": [1, 2, 3, 4], "b": [10, 20, 30, 40]})
dfs = pd.DataFrame({"a": [1, 2, 3, 4], "b": [10, 20, 30, 40]})
print(df_non_colours)


# Обработаем датасет в мультипроцессорном режиме с замером времени
# (удалим из текста html-теги, неалфавитные символы, переведём в нижний регистр)

start_time = dt.datetime.now()
print("ВРЕМЯ СТАРТА РАСЧЁТА:", start_time, "\n")

# Запарралелим расчёты между доступными ядрами процессора:

# 1. рассчитываем количество ядер процесса, которые задействуем для вычислений
#    (уменьшаем на 1 ядро, которое оставляем на системные потребности)
n_cpu = multiprocessing.cpu_count() - 1
print("Количество доступных процессоров:", n_cpu)

# 2. Расчитаем размер обрабатываемого парралельно подмассива
val_sub = int(len(df_non_colours) / n_cpu)
print("Размеры подмассивов:", val_sub, "\n")

# 3. Создаём менеджера парралельных процессов
#    и его пространство имён для обмена данными между процессами
if __name__ == "__main__":
    with Manager() as mng:
        ns = mng.Namespace()
        ns.dfsmp = mng.list()
        ns.df = dfs
        # 4. Делим датасет на составляющие,
        #    которые будут рассчитываться в парралельных процессах
        for i in range(n_cpu - 1):
            ns.dfsmp.append((df_non_colours[val_sub * i : val_sub * (i + 1)], ns.df))
        ns.dfsmp.append((df_non_colours[(n_cpu - 1) * val_sub :], ns.df))
        print(
            len(ns.dfsmp),
            type(ns.dfsmp),
            type(ns.dfsmp[0]),
            type(ns.dfsmp[0][0]),
            type(ns.dfsmp[0][1]),
        )

        # 5. Запустим пул парралельных процессов вычислений
        #    и объединим результат в единый датафрейм
        with Pool(processes=n_cpu) as p:
            df_non_colours = pd.concat(
                list(p.map(add_freq_product_color, ns.dfsmp)), axis=0
            )

finish_time = dt.datetime.now()
print("\n\nВРЕМЯ ОКОНЧАНИЯ РАСЧЁТА:", finish_time)
print("ВРЕМЯ ВЫПОЛНЕНИЯ:", finish_time - start_time, "\n" * 2)
