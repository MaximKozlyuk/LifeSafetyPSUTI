from math import sqrt

from src.lab2.showers import ShowersTable
from src.properties import PropertiesFile

"""
  Вариант 11
  душ: ПДВ    x = 0.65 м  vв = 1.5 м/с
  tрз = 23.9  tнм = 22.0
  Срз = 16.7  С0 = 8.7  ПДК = 13.2 мг/м^3
"""


class DefaultShowerCalculation(object):
    """Содежрит расчеты душа для случая Pt < 0.6"""

    def F0_1(self, Pt_, x_, m_, n_):
        return (Pt_ * x_ / (0.6 * n_)) ** 2

    def V0(self, Uv_, x_, F0_, m_):
        print()     # todo implement


class IntermediateCase(DefaultShowerCalculation):
    """Содежрит расчеты душа для случая 1 > Pt >= 0.6"""

    def F0_1(self, Pt_, x_, m_, n_):
        return ((x_ + 5.3 * Pt_ - 3.2) / (0.75 * n_)) ** 2

    def V0(self, Uv_, x_, F0_, m_):
        return Uv_ / (0.7 + 0.1 * (0.8 * m_ * (F0_ ** (1/2)) - x_))


class OneCase(DefaultShowerCalculation):
    """Содежрит расчеты душа для случая Pt = 1"""
    def F0_1(self, Pt_, x_, m_, n_):
        return (x_ / (0.8 * m_)) ** 2


def choose_calculation(Pt_):
    if Pt_ < 0.6:  # DefaultShowerCalculation
        return DefaultShowerCalculation()
    elif 1 > Pt_ >= 0.6:  # IntermediateCase
        return IntermediateCase()
    elif Pt_ == 1:  # OneCase
        return OneCase()
    else:
        raise Exception("значение Pt расчитанно некорректно")


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
print("t0 =", str(t0), "°С\nОтношение разностей температур:")
Pt = (t_rz - t_norm) / (t_rz - t0)
print("Pt =", Pt)

# 2
subtypes = showers_table.subtypes(shower_type)
shower_calculation = choose_calculation(Pt)
shower = None
for i in subtypes:
    f0_1 = shower_calculation.F0_1(Pt, x, i.m(), i.n)
    if f0_1 < i.square:
        shower = i
        break
if shower is None:
    raise Exception("Тип душа не определен")
print("Выбранный душ:", shower, "F0 =", shower.square, "м^2")

# 3 Uv_, x_, F0_, m_
V0 = shower_calculation.V0(Uv, x, shower.square, shower.m())
print("Скорость выхода воздуха =", V0, "м/с^2")

input("Press ENTER to exit program.")
exit(0)
