import math

def exponential_decay(a: float, k: float, r: float) -> float:
    return a * math.e**(-k * r)