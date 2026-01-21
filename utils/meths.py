import random
from math import cos, e, log, radians, sin
from typing import Literal

Number = int | float
Red, Green, Blue = (Number, Number, Number)
RGB = tuple[Red, Green, Blue]

def exponential_decay_formula(a: Number, k: Number, r: Number) -> Number:
    return a * e**(-k * r)

def hue_base(angles: tuple[Number, ...]) -> RGB | tuple[Number, ...]:
    return tuple(angle / 360 for angle in angles)

def k_rate(alpha_list: tuple[Number, ...]) -> Number:
    log_sum = sum(-log(a) for a in alpha_list)
    return log_sum / len(alpha_list)

def opacity_rate(a: Number, r: Number, alpha_list: tuple[Number, ...]) -> Number:
    k = k_rate(alpha_list)
    return exponential_decay_formula(a, k, r)

def gradient_coords(angle) -> tuple[Number, Number, Number, Number]:
    rad = radians(angle)
    
    x1 = 50 - 50 * cos(rad)
    y1 = 50 - 50 * sin(rad)
    x2 = 50 + 50 * cos(rad)
    y2 = 50 + 50 * sin(rad)
    
    return x1, y1, x2, y2
