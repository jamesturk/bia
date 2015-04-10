import decimal


def remove_exponent(d):
    return d.quantize(decimal.Decimal(1)) if d == d.to_integral() else d.normalize()


def round_to(number, increment, up_threshold=0.95):
    """ round number to nearest multiple of increment """
    ratio = number/increment
    whole = ratio.to_integral(rounding=decimal.ROUND_DOWN)
    dec = ratio - whole
    if dec >= up_threshold:
        whole += 1
    return whole * increment


def to_lb(weight_kg):
    return remove_exponent(round_to(weight_kg * decimal.Decimal("2.2046"),
                                    decimal.Decimal("0.125")))
