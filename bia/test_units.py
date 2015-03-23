from .units import Mass


def test_basic_conversions():
    a = Mass(2, 'kg')
    kg = a.as_unit('kg')
    assert kg.scalar == 2
    assert kg.unit == 'kg'

    lb = a.as_unit('lb')
    assert abs(lb.scalar - 4.40925) < 0.0001
    assert lb.unit == 'lb'

    g = a.as_unit('g')
    assert abs(g.scalar - 2000) < 0.0001
    assert g.unit == 'g'

    assert g.as_unit('lb').scalar == a.as_unit('lb').scalar
