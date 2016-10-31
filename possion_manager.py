import random
import math


class NegativeExponentialDist(object):
    def __init__(self, l):
        self.L = l

    def produce_random_num(self):
        """
        negative exponential distribution
        return a double random number, L is the mean value
        """
        u = random.random()
        return -self.L * math.log(u)

    def produce_mass_random_num(self, n):
        for v in range(n):
            yield self.produce_random_num()


def depend_direction(p):
    a = random.uniform(0, 1)
    return True if a < p else False


if __name__ == "__main__":
    pass

