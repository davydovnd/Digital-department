import numpy as np
import pandas as pd

# Загрузка данных эталона
data = np.loadtxt("исходные данные.txt", comments='#', usecols=(0, 1, 2, 3))

# Загрузка данных для вычисления ошибки
data1 = np.loadtxt("вычисление ошибки.txt", comments='#', usecols=(0, 1))

# Занрузка данных эксперимента
data2 = np.loadtxt("данные эксперимента.txt", comments='#', usecols=(0, 1, 2))

# Загрузка банка фаз
new = pd.read_csv("DataPhases.csv")

# Расчет среднего значения постоянной электронографа
Cav = (data[:, 1] * data[:, 3]).mean()

# Расчет среднего значения радиуса конуса
Rav = data1[:, 1].mean()

# Расчет среднего значения отклонения радиуса от эталона
dRav = (data[0, 1] - data1[:, 1]).mean()

# Расчет погрешности значения постоянной электронографа
dCav = (dRav * data[:, 3]).mean()

# Расчет межплоскостного расстояния
dHKL = Cav / (data2[:, 2])

# Расчет погрешности значения межплоскостного расстояния
ddHKL = dCav/(data2[:, 2]) + (- Cav * dRav / (data2[:, 2]) / (data2[:, 2]))

# Сортировка банка фаз
Al = new.iloc[:5:, 2].iloc[:: -1].astype('float64').to_numpy()
CoCr2O4 = new.iloc[6:12:, 2].iloc[:: -1].astype('float64').to_numpy()
CuMg2 = new.iloc[13:19:, 2].iloc[:: -1].astype('float64').to_numpy()
Fe2O3 = new.iloc[20:25:, 2].iloc[:: -1].astype('float64').to_numpy()
Hg = new.iloc[26:31:, 2].iloc[:: -1].astype('float64').to_numpy()
Li = new.iloc[32:36:, 2].iloc[:: -1].astype('float64').to_numpy()
SiC = new.iloc[37:43:, 2].iloc[:: -1].astype('float64').to_numpy()
UCl4 = new.iloc[44:49:, 2].iloc[:: -1].astype('float64').to_numpy()
V = new.iloc[50:55:, 2].iloc[:: -1].astype('float64').to_numpy()
W = new.iloc[56:63:, 2].iloc[:: -1].astype('float64').to_numpy()
phase_dict= dict(zip([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [Al, CoCr2O4, CuMg2, Fe2O3, Hg, Li, SiC, UCl4, V, W]))
name_dict = dict(zip([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ["Al", "CoCr2O4", "CuMg2", "Fe2O3", "Hg", "Li", "SiC", "UCl4", "V", "W"]))

# Проведение фазового качественного анализа - сравнение ряда dHKL
def phase_analysis(phase, phase_name):
    i = 0
    for i in range(3):
        if (round(dHKL[i] - abs(ddHKL[i]), 2) <= phase[i]) and (phase[i] <= round(dHKL[i] + abs(ddHKL[i]), 2)):
            i += 1
    if i == 3:
        return f"!!!!! Фаза {phase_name} найдена в образце !!!!!"
    else:
        return f"Фаза {phase_name} в образце отсутствует"

print('Расчет ошибки вычисления радиуса:')
print(f'Rср = ({round(Rav,1)} +- {round(dRav,1)}) - радиус конуса')
print()
print('Расчет постоянной электронографа:')
print(f'Cср = ({round(Cav,1)} +- {round(dCav,1)}) - постоянная электронографа')
print()
print('Проведение качественного фазового анализа:')
j = 0
for j in range(10):
    j += 1
    print(phase_analysis(phase_dict[j], name_dict[j]))

# Выгрузка данных качественного фазового анализа
with open("Results.txt", "w") as text_file:
    print('Расчет ошибки вычисления радиуса:', file=text_file)
    print(f'Rср = ({round(Rav, 1)} +- {round(dRav, 1)}) - радиус конуса', file=text_file)
    print('', file=text_file)
    print('Расчет постоянной электронографа:', file=text_file)
    print(f'Cср = ({round(Cav, 1)} +- {round(dCav, 1)}) - постоянная электронографа', file=text_file)
    print('', file=text_file)
    print('Проведение качественного фазового анализа:', file=text_file)
    j = 0
    for j in range(10):
        j += 1
        print(phase_analysis(phase_dict[j], name_dict[j]), file=text_file)
