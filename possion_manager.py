import random
import math


def expntl(L):
    """
    negative exponential distribution
    return a double random number, L is the mean value
    """
    u = random.random()
    return -L * math.log(u)

if __name__ == "__main__":
    for i in range(100):
        print expntl(3)

