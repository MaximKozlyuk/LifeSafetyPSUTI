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
    """Базовый класс для логики расчета пункта Б"""
    def __init__(self) -> None:
        super().__init__()

    def resolvePkCase(self, Pk_):
        try:
            if Pk_ < 0.4:
                return LowPkCalculations()
            else:
                return HighPkCalculations()
        except Exception as e:
            print(e)
            raise Exception("Ошибка при выборе метода расчета в зависимости от Pk")

    # todo 2 разные формулы в методичке ??? (C_rz_ - PDK_) * (C_rz_ - C0_)
    def Pk(self, C_rz_, C0_, PDK_):
        return (C_rz_ - PDK_) / (C_rz_ - C0_)


# todo implement
class LowPkCalculations(HarmfulSubstances):
    """Расчеты при PK < 0.4"""
    def __init__(self) -> None:
        super().__init__()

    def F0_1(self, x_, Pk_, n_):
        raise Exception("Функционал не реализованн")

    def V0(self, Uv_, m_, F0_, x_):
        raise Exception("Функционал не реализованн")

    def tox(self, t_rz_, t_norm_, n_, F0_, x_):
        raise Exception("Функционал не реализованн")


class HighPkCalculations(HarmfulSubstances):
    """Расчеты при PK >= 0.4"""
    def __init__(self) -> None:
        super().__init__()

    def F0_1(self, x_, Pk_, n_):
        return ((x_ + 3.7 * Pk_ - 1.5) / (0.75 * n_)) ** 2

    def V0(self, Uv_, m_, F0_, x_):
        sub_big = (0.8 * m_ * (F0_ ** (1/2)) - x_)
        big = (0.55 + 0.14 * sub_big)
        return Uv_ / big

    def tox(self, t_rz_, t_norm_, n_, F0_, x_):
        return t_rz_ - ((t_rz_ - t_norm_) / (0.45 + 0.25 * (0.75 * n_ * (F0_ ** (1/2)) - x_)))


def resolve_m_val(m_):
    m_alpha = None
    m_val = None
    if type(m_) is not float:
        m_alpha = float(m_[1])
        m_val = float(m_[0])
        return m_val
    else:
        return m_


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
m = resolve_m_val(shower.m())
V0 = shower_calculation.V0(Uv, x, shower.square, m)
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
harmful_substances = HarmfulSubstances()

# 1
Pk = harmful_substances.Pk(C_rz, C0, PDK)
print("1. Отношение концентраций:")
print("Pk =", Pk)
harmful_substances = harmful_substances.resolvePkCase(Pk)

# 2
print("2. Площадь живого сечения:")
harmful_F0_1 = harmful_substances.F0_1(x, Pk, shower.n)
print("F0' =", harmful_F0_1, "м^2")

# 3
print("3. Скорость выхода воздуха:")
harmful_V0 = harmful_substances.V0(Uv, resolve_m_val(shower.m()), shower.square, x)
print("V0 =", harmful_V0, "м/с")

# 4
print("Температура на выходе патрубка:")
harmful_tox = harmful_substances.tox(t_rz, t_norm, shower.n, shower.square, x)
print("tox =", harmful_tox, "°С")

input("\nPress ENTER to exit program.")
exit(0)
