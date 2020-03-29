from src.util.properties import CSVFile


class Shower(object):
    """
        Класс - представляет строчку из файла-перечня душов.
        Нужен для удобной работы с размерами (диаметр или длинна с шириной), а также же m c альфа значением
    """
    def __init__(self, name, size, square, m, n, z) -> None:
        self.name = name
        self.__size = size
        self.square = float(square)     # F0
        self.__m = m
        self.n = float(n)
        self.z = float(z)
        super().__init__()

    @staticmethod
    def __split(delimiter, data):
        split = str(data).split(delimiter)
        map(float, split)
        return split

    def size(self):
        if "x" in str(self.__size):
            return self.__split("x", self.__size)
        elif "X" in str(self.__size):
            return self.__split("X", self.__size)
        else:
            return float(self.__size)

    def m(self):
        if " " in str(self.__m):
            return self.__split(" ", self.__m)
        else:
            return float(self.__m)

    def __str__(self) -> str:
        return self.name


class ShowersTable(CSVFile):

    def __init__(self, file_name) -> None:
        self.showers = []
        super().__init__(file_name)

    def read_values(self):
        super().read_values()
        self.showers = []
        for i in self.values:
            self.showers.append(
                Shower(i[0], i[1], i[2], i[3], i[4], i[5])
            )
        return self.showers

    def subtypes(self, t):
        types = []
        for i in self.showers:
            if t in i.name:
                types.append(i)
        return types
