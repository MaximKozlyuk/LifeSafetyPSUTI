

class DefaultShowerCalculation(object):
    """Содежрит расчеты душа для случая Pt < 0.6"""

    def __init__(self) -> None:
        self.Xht_mem = None
        self.L0_mem = None
        super().__init__()

    def F0_1(self, Pt_, x_, m_, n_):
        return (Pt_ * x_ / (0.6 * n_)) ** 2

    def V0(self, Uv_, x_, F0_, m_):
        print()     # todo implement

    def L0(self, F0_, V0_):
        self.L0_mem = F0_ * V0_
        return self.L0_mem

    def Xht(self, n_, F0_):
        self.Xht_mem = 0.6 * n_ * (F0_ ** (1/2))
        return self.Xht_mem

    def tox(self, x_, t_rz_, t_norm_):
        if x_ < self.Xht_mem:
            return t_norm_
        else:
            return t_rz_ - x_ * ((t_rz_ - t_norm_) / self.Xht_mem)


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
