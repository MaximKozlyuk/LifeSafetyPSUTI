import math


class __HoodOneTwo(object):

    def U_m(self, Q, r, h):
        return 0.0425 * ((Q / r) ** (1 / 3)) * ((h / r) ** (1 / 3))

    def L_str(self, r, U_m):
        return ((math.pi * (r ** 2)) / 3) * U_m


class HoodConfiguration1(__HoodOneTwo):

    def L1_prot(self, R, r):
        return 3 - (2 * (R / r))


class HoodConfiguration2(__HoodOneTwo):

    def L1_prot(self, R, r):
        return 3.4 - 2.4 * (R / r)


class HoodConfiguration3(object):

    def L1_prot(self, A, a):
        return 3.1 - 2.1 * (A / a)

    def U_m(self, Q, hp, b):
        return 0.03 * (Q ** (1/3)) * ((hp / b) ** 0.38)

    def L_str(self, a, b, U_m):
        return a * b * U_m


class ExhaustHood(object):
    """Агригатор схем зонтов, параметры должен принимать в порядке как в функциях классов HoodConfiguration"""

    __types_set = [1, 2, 3]

    def __init__(self, hood_type) -> None:
        if hood_type not in self.__types_set:
            raise Exception("Нельзя создать рукав с таким типом")
        self.hood_type = hood_type
        self.configs = []
        self.configs.append(HoodConfiguration1())
        self.configs.append(HoodConfiguration2())
        self.configs.append(HoodConfiguration3())
        super().__init__()

    def L1_prot(self, params):
        """
        :param params:
            1) R, r
            2) R, r
            3) A, a
        """
        return self.configs[self.hood_type - 1].L1_prot(params[0], params[1])

    def U_m(self, params):
        """
        :param params:
            1) Q, r, h
            2) Q, r, h
            3) Q, hp, b
        """
        return self.configs[self.hood_type - 1].U_m(params[0], params[1], params[2])

    def L_str(self, params):
        """
        :param params:
            1) r, U_m
            2) r, U_m
            3) a, b, U_m
        """
        if len(params) == 2:
            return self.configs[self.hood_type - 1].L_str(params[0], params[1])
        elif len(params) == 3:
            return self.configs[self.hood_type - 1].L_str(params[0], params[1], params[2])
        else:
            raise Exception("Непредвиденное количесвто параметров", params)
