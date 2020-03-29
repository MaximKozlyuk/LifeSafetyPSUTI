from math import sqrt

from src.lab2.heat_removing import choose_calculation
from src.lab2.showers import ShowersTable
from src.properties import PropertiesFile

"""
  программа работает не для всех вариантов
  
  Вариант 11
  душ: ПДВ    x = 0.65 м  vв = 1.5 м/с
  tрз = 23.9  tнм = 22.0
  Срз = 16.7  С0 = 8.7  ПДК = 13.2 мг/м^3
"""


class HarmfulSubstances(object):
    """Содержит в себе логику расчета пункта Б для случая Pk < 0.4"""
    def __init__(self) -> None:
        super().__init__()


props = PropertiesFile("lab2.properties")
properties = props.properties("=")

showers_table = ShowersTable("air_showers.csv")
showers_table.read_values()

# Инициализация переменных для расчета
shower_type = properties[0][1]
x = properties[1][1]
Uv = properties[2][1]
t_rz = properties[3][1]
t_norm = properties[4][1]
C_rz = properties[5][1]
C0 = properties[6][1]
PDK = properties[7][1]

print("А. Удаление избытков тепла")

# 1
print("1. Вычисляем температуру на выходе патрубка:")
t0 = t_norm - 1.0
print("t0 =", str(t0), "°С")
print("Отношение разностей температур:")
Pt = (t_rz - t_norm) / (t_rz - t0)
print("Pt =", Pt)

# 2
subtypes = showers_table.subtypes(shower_type)
shower_calculation = choose_calculation(Pt)
shower = None
F0_1 = None
for i in subtypes:
    F0_1 = shower_calculation.F0_1(Pt, x, i.m(), i.n)
    if F0_1 < i.square:
        shower = i
        break
if shower is None:
    raise Exception("Тип душа не определен")
print("2. Выбранный душ:")
print(shower, "F0 =", shower.square, "м^2")

# 3
V0 = shower_calculation.V0(Uv, x, shower.square, shower.m())
print("3. Скорость выхода воздуха:")
print("V0 =", V0, "м/с^2")

# 4
L0 = shower_calculation.L0(shower.square, V0)
print("4. Обьем воздуха, проходящего через душ:")
print("L0 =", L0, "м^3/c")

# 5
Xht = shower_calculation.Xht(shower.n, shower.square)
print("5. Длинна начального участка воздушной струи:")
print("Xht =", Xht, "м")

# 6
tox = shower_calculation.tox(x, t_rz, t_norm)
print("6. Температура воздуха на выходе патрубка =")
print("tox =", tox, "°С")

print("\nБ. Удаление вредных веществ")

# 1

print("1. Отношение концентраций")

input("Press ENTER to exit program.")
exit(0)
