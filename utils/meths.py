import math
import random
from typing import Literal

Number = int | float
Red, Green, Blue = (Number, Number, Number)
RGB = tuple[Red, Green, Blue]

X, Y = Number, Number
Point = tuple[X, Y]

def exponential_decay_formula(a: Number, k: Number, r: Number) -> Number:
    return a * math.e**(-k * r)

# def k_rate(alpha_list: tuple[Number, ...]) -> Number:
#     log_sum = sum(-math.log(a) for a in alpha_list)
#     return log_sum / len(alpha_list)

# def opacity_rate(a: Number, r: Number, alpha_list: tuple[Number, ...]) -> Number:
#     k = k_rate(alpha_list)
#     return exponential_decay_formula(a, k, r)

def radius_energy(points: tuple[Point, ...]) -> None:
    return sum(x*x + y*y for x, y in points) / len(points)

def area_compensate(base_points, morph_points):
    R0_sq = radius_energy(base_points)
    R1_sq = radius_energy(morph_points)

    if R1_sq == 0:
        raise ValueError("Degenerate morph shape: zero radius energy")

    s = math.sqrt(R0_sq / R1_sq)

    scaled = [(s * x, s * y) for x, y in morph_points]

    return scaled, s