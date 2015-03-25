import math


def one_rm_epley(weight, reps):
    return weight * (1 + (reps / 30.0))

def one_rm_brzycki(weight, reps):
    return weight * (36 / (37.0 - reps))

def one_rm_lander(weight, reps):
    return (100 * weight) / (101.3 - 2.67123 * reps)

def one_rm_lombardi(weight, reps):
    return weight * (reps ** 0.1)

def one_rm_mayhew(weight, reps):
    return (100 * weight) / (52.2 + 41.9 * math.e ** (-0.055*reps))

def one_rm_oconner(weight, reps):
    return weight * (1 + 0.025 * reps)

def one_rm_wathen(weight, reps):
    return (100 * weight) / (48.8 + 53.8 * math.e ** (-0.075*reps))
