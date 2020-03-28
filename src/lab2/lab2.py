from math import sqrt

from src.properties import PropertiesFile, CSVTable

"""
  Вариант 11
  душ: ПДВ    x = 0.65 м  vв = 1.5 м/с
  tрз = 23.9  tнм = 22.0
  Срз = 16.7  С0 = 8.7  ПДК = 13.2 мг/м^3
"""


class ShowersTable(CSVTable):

    def shower_subtypes(self, t):
        subtypes = []
        for i in self.values:
            if str(t) in str(i[0]):
                subtypes.append(i[0])
        return subtypes


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
print(showers_table.shower_subtypes(shower_type))

input("Press ENTER to exit program.")
exit(0)
