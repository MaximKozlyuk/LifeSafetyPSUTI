import math


def screen_radius(length, width, deep):
    return 0.62 * (length * width * deep) ** (1 / 3)


# x = ß * screen_radius
# ß = 2π/a   (a - длинна волны)
def param_A(x):
    return ((1 + (x ** 6)) / (x ** 2)) ** (1 / 2)


def param_B(x):
    return 1 + (x ** 2)


def beta(a_i):
    return (2 * math.pi) / a_i


# Формулы для различных типов экранов
# формула 3.1
def metal_screen():
    return 0


# формула 3.2   todo end
def metal_net_screen(psi_, zi, E_or_H, ro):
    return psi_ * ((de_e(1, 2)) ** (1/2))


# dэ
def de_e(r_, s_):
    return (math.pi * (r_ ** 2)) / s_


# формула 3.3
def paint_screen():
    return 0


# формула 3.4
# d - толщина металла
def thin_metal(psi_, Zi, d_, p_):
    return psi_ * 1.25 * math.pi * ((d_ * (Zi / p_)) ** (1/2))


def psi(m_, a_i, sr_):
    return ((1 - ((math.pi * m_) / a_i)) ** 6) * math.pow((a_i / sr_), 1/3)


print("БЖД лабораторная работа 3")
print("Расчет эффективности экранирования\n")

# Ввод исходных данных
chooseScreenTypeMsg = """Выберете тип защитного экрана (номер формулы):
1. металлический экран (3.1)
2. экран из металлической сетки (3.2)
3. экран из токопроводящей краски (3.3)
4. экран из тонкого металла (3.4)
(введите номер от 1 до 4)
"""
screen_type = input(chooseScreenTypeMsg)
print("screen_type = ", screen_type)
screen_func = None
if screen_type == "1":
    screen_func = metal_screen
elif screen_type == "2":
    screen_func = metal_net_screen
elif screen_type == "3":
    screen_func = paint_screen
elif screen_type == "4":
    screen_func = thin_metal
else:
    raise Exception("Неверно выбран тип защитного экрана")

# todo prompt for all params
# число декадных длин волн
N = 4
# размеры экрана (м)
b = 2.5
l = 1.0
h = 1.5
# линейный размер щелей (мм)
m = 40.0
# радиус проволоки (мм)
rs = 0.03
# шаг сетки экрана (мм)
s = 0.2
# минимальна длинна волны (м) (lv в вариантах)
a_min = 0.2
# толщина металла (мм)
d = 0.01
# удельное сопротивление на низких частотах (Ом * м)
p = 10 ** (-7)

# Расчеты
# 1
sr = screen_radius(b, l, h)
print("Эквивалентный радиус экрана =", sr)

# 2
ai = []
for i in range(0, N + 1):
    ai.append(a_min * (10 ** i))
print("Длинны волн:", ai, "\n")

# 3
Z0 = 120.0 * math.pi
xi = []
Ai = []
Bi = []
beta_i = []
Ze = []
Zh = []
psi_i = []
for i in range(0, N+1):
    beta_i.append(beta(ai[i]))
    xi.append(sr * beta_i[i])
    Bi.append(param_B(xi[i]))
    Ai.append(param_A(xi[i]))
    Ze.append(Z0 * (Ai[i] / Bi[i]))
    Zh.append(Z0 * (Bi[i] / Ai[i]))
    psi_i.append(psi(m / 1000, ai[i], sr))  # m - приводим миллиметры к метрам
    print("Расчет для a", i, "=", ai[i])
    print("β =", beta_i[i], "x =", xi[i])
    print("A =", Ai[i], "B =", Bi[i])
    print("Ze =", Ze[i], "Zh =", Zh[i])
    print("Ψ‎ =", psi_i[i])
    # todo if screen_type == 1 ... elif ... to resolve different func params
    print("ЭЭЕ =", screen_func(psi_i[i], Ze[i], d / 1000, p), "ЭЭН =", screen_func(psi_i[i], Zh[i], d / 1000, p))
    print()

# 4
# todo Постройте зависимости ЭЭE(λ), ЭЭH(λ) по анало- гии с рис. 3.1,3.2.


print("Расчет окончен")
