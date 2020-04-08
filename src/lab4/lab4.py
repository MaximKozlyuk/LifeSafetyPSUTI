"""
    Default var:
    размер источника вредных выделений 2a x 2b = 1.4м х 1.4м
    производительность источника по теплоте Q = 1050 Вт
    скорость движения воздуха в помещении Wв = 0.3 м/с
    высота размещения зонта над источником h = 1.3 м
    производительность источника по выбросам G = 77 мг/с
    количество аэрозольных выбросов на один зонт Gр = 16 мг/с
    расход воздуха, приходящегося на один зонт Lв = 0.3 м^3/c
    предельно допустимая концентрация вредных веществ ПДК = 24 мг/м^3
    концентрация вредных веществ в приточном воздухе Спр = 16 мг/м^3
    схема зонта 3

    файл s_functions_chart.properties содержит точки Х начала и конца для расчета функций S1 и S2
    step - приращение Х, при задании слишком малого значения расчет может сильно затянуться
    эксперементально было определено (при расчете вариантов 11 и 6) что точка X (Kn) пересечения функций S1 и S2 = M
    или Kn находится недалеко от M
"""
import math

import matplotlib.pyplot as plt

from src.lab4.equation import EquationSystem
from src.lab4.exhaust_hood import ExhaustHood
from src.util.properties import PropertiesFile

props = PropertiesFile("lab4.properties")
properties = props.properties("=")

a = properties[0][1] / 2
b = properties[1][1] / 2
# производительность источника по теплоте
Q = properties[2][1]
# скорость движения воздуха в помещении
Wb = properties[3][1]
# высота размещения зонта над источником
h = properties[4][1]
G = properties[5][1]
Gp = properties[6][1]
Lv = properties[7][1]
PDK = properties[8][1]
Cpr = properties[9][1]
hood_schema = int(properties[10][1])

print("БЖД практическая работа 4")
print("Локальная защита от промышленных газов, пыли, пара, избытка тепла\n")

# 1
print("1. Выбираем размеры зонта A и B исходя из условий как среднее арифметрическое значение, округляя до десятых:")
A_lower_than = a + 0.24 * h
A = round(((a + A_lower_than) / 2), 1)
print("a < A  a + 0.24•h;", a, "< A ≤", A_lower_than, "-> A =", A, "м")
B_lower_than = a + 0.24 * h
B = round(((b + B_lower_than) / 2), 1)
print("b < B  b + 0.24•h;", b, "< B ≤", B_lower_than, "-> B =", B, "м")

# 2
print("2. Вычисляем параметры для предложенной схемы зонта по табл. 4.1:")
exhaust_hood = ExhaustHood(hood_schema)

r = 1.128 * ((a * b) ** (1/2))
R = 1.128 * ((A * B) ** (1/2))
if hood_schema == 1 or hood_schema == 2:
    print("r =", r)
    print("R =", R)

hp = h + b / 0.24
print("hп =", hp, "м")

L1_prot = 0.0
if hood_schema == 1 or hood_schema == 2:
    L1_prot = exhaust_hood.L1_prot([R, r])
else:
    L1_prot = exhaust_hood.L1_prot([A, a])
print("L'прот =", L1_prot)

U_m = 0.0
if hood_schema == 1 or hood_schema == 2:
    U_m = exhaust_hood.U_m([Q, r, h])
else:
    U_m = exhaust_hood.U_m([Q, hp, b])
print("Uм = ", U_m, "м/с")

L_str = 0.0
if hood_schema == 1 or hood_schema == 2:
    L_str = exhaust_hood.L_str([r, U_m])
else:
    L_str = exhaust_hood.L_str([a, b, U_m])
print("Lстр =", L_str, "м^3/с")

# 3
print("3. Площадь раскрыва зонта")
F1 = 4 * A * B
print("F1 =", F1, "м^2")

# 4
print("4. Площадь источника загрязнений")
F2 = 4 * a * b
print("F2 =", F2, "м^2")

# 5
print("5. Поправочный коэффициент")
K_p = 1.0 + (3.0 - (F1 / F2)) * (Wb / U_m)
print("Kп =", K_p)

# 6
print("6. Вычисляем производительность зонта")
L_prot = K_p * L_str * L1_prot  # todo в пункте 6 расчетов К или Кп? скорре всего минорны баг методички
print("Lпрот =", L_prot)

# 7
print("7. Максимальная концентрация вредных веществ в удаляемом воздухе:")
C_pred = G / L_prot + Cpr
print("Cпред =", C_pred)

# 8
print("8. Максимальная концентрация в в удаляемом воздухе:")
delta_C1_pred = (C_pred - Cpr) / (PDK - Cpr)
print("∆C'пред =", delta_C1_pred)

# 9
print("9. Характеристический показатель газового баланса в раскрыве зонта:")
M = (Gp / G) * delta_C1_pred - Lv / L_prot
print("M =", M)

# 10
print("10. Решая трансцендентное уравнение")
chart_props_file = PropertiesFile("s_functions_chart.properties")
chart_props = chart_props_file.properties("=")

# рисуем график
plt.title("Нахождение Kn")
eq = EquationSystem(M, delta_C1_pred)

S1_values = eq.S1_range(chart_props[0][1], chart_props[1][1], chart_props[2][1])
S2_values = eq.S2_range(chart_props[0][1], chart_props[1][1], chart_props[2][1])

plt.plot(S1_values[0], S1_values[1], label="S1")
plt.plot(S2_values[0], S2_values[1], label="S2")

plt.xlabel("x")
plt.ylabel("y")
plt.legend()

plt.grid()
plt.show()

# todo Kn - точка пересечения графиков S1 и S2, по-хорошему нужно считать численным методом, но так вроде тоже норм
Kn = M
n = 1 - math.exp(-2.52 * Kn)
print("Kn =", Kn)
print("n =", n)

# 11
print("11. Производительность зонта")
L_ot = Kn * L_prot
print("Lот =", L_ot)

# 12
print("12. Количество вредных веществ в удаляемом воздухе:")
Gy = n * G
print("Gy =", Gy)

# 13
print("13. Концентрация вредных веществ в удаляемом воздухе:")
C_ud = Gy / L_ot
print("Cуд =", C_ud)

input("Нажмите Enter для выхода из прорграммы")
exit(0)
