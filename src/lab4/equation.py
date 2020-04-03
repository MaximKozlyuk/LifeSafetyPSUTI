import math


class EquationSystem(object):

    def __init__(self, M, delta_C1_pred) -> None:
        self.M = M
        self.delta_C1_pred = delta_C1_pred
        super().__init__()

    def S1(self, Kn):
        return 2.52 * Kn

    def S2(self, Kn):
        return - math.log((Kn - self.M) / self.delta_C1_pred)

    def S1_range(self, begin, end, step):
        return self.__func_range(begin, end, step, self.S1)

    def S2_range(self, begin, end, step):
        return self.__func_range(begin, end, step, self.S2)

    def __func_range(self, begin, end, step, func):
        y = []
        x = []
        while begin < end:
            try:
                v = func(begin)
                y.append(v)
            except Exception:
                y.append(0.0)
            x.append(begin)
            begin += step
        return x, y
