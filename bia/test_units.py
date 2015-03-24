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


def test_basic_cmp():
    assert Mass(1, 'kg') < Mass(2, 'kg')
    assert Mass(1, 'kg') <= Mass(2, 'kg')
    assert Mass(2, 'kg') <= Mass(2, 'kg')
    assert Mass(2, 'kg') == Mass(2, 'kg')
    assert Mass(2, 'kg') >= Mass(2, 'kg')
    assert Mass(2, 'kg') > Mass(1, 'kg')
    assert Mass(2, 'kg') >= Mass(1, 'kg')


def test_conversion_cmp():
    assert Mass(1, 'kg') < Mass(100, 'lb')
    assert Mass(1000000, 'g') > Mass(100, 'lb')


def test_addition():
    assert Mass(1, 'kg') + Mass(2, 'kg') == Mass(3, 'kg')
    assert Mass(1, 'kg') + Mass(1, 'lb') > Mass(1.4, 'kg')


def test_subtraction():
    assert Mass(2, 'kg') - Mass(1, 'kg') == Mass(1, 'kg')
    assert Mass(1, 'kg') - Mass(1, 'lb') < Mass(0.55, 'kg')
