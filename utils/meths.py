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

def hue_base(angles: tuple[Number, ...]) -> RGB | tuple[Number, ...]:
    return tuple(angle / 360 for angle in angles)

def k_rate(alpha_list: tuple[Number, ...]) -> Number:
    log_sum = sum(-math.log(a) for a in alpha_list)
    return log_sum / len(alpha_list)

def opacity_rate(a: Number, r: Number, alpha_list: tuple[Number, ...]) -> Number:
    k = k_rate(alpha_list)
    return exponential_decay_formula(a, k, r)

def gradient_coords(angle) -> tuple[Number, Number, Number, Number]:
    rad = math.radians(angle)
    
    x1 = 50 - 50 * math.cos(rad)
    y1 = 50 - 50 * math.sin(rad)
    x2 = 50 + 50 * math.cos(rad)
    y2 = 50 + 50 * math.sin(rad)
    
    return x1, y1, x2, y2

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

if __name__ == '__main__':
    base_points = (
         (-50, -50),
         (0, -80), (50, -50), (50, 0),
         (50, 50), (0, 80), (-50, 50),
         (-50, 0), (-30, 20), (-50, -50))
    morph_points = (
         (-100,-10),
         (0,-70), (60,-40), (50,10),
         (40,60), (0,70), (-40,50),
         (-50,0), (-30,-30), (-60,-40))

    res = area_compensate(base_points, morph_points)
    print(res)