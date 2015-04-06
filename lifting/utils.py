import decimal


def round_to(number, increment, up_threshold=0.95):
    """ round number to nearest multiple of increment """
    ratio = number/increment
    whole = ratio.to_integral(rounding=decimal.ROUND_DOWN)
    dec = ratio - whole
    if dec >= up_threshold:
        whole += 1
    return whole * increment
