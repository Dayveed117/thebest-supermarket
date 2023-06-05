class Fitness():
    """
    Fitness for any chromossom
    """

    @classmethod
    def fun1(cls, chrom):
        return sum(chrom) / len(chrom)

    @classmethod
    def fun2(cls, chrom):
        x = chrom[0]
        y = chrom[1]

        # Division by 0 not treated
        eq1 = abs(2*x + y - 9)
        eq2 = abs(x*x - y - 2)

        return 1 / (eq1 + eq2)
