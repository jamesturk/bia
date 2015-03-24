from .units import Unit
from .units import UnitValue as V


def test_unit_basics():
    assert Unit('kg') == Unit(['kg'])
    assert Unit(['kg'], ['m']) == Unit(['kg'], ['m'])


def test_basic_conversions():
    a = V(2, 'kg')
    kg = a.as_unit('kg')
    assert kg.scalar == 2
    assert kg.unit == Unit('kg')

    lb = a.as_unit('lb')
    assert abs(lb.scalar - 4.40925) < 0.0001
    assert lb.unit == Unit('lb')

    g = a.as_unit('g')
    assert abs(g.scalar - 2000) < 0.0001
    assert g.unit == Unit('g')

    assert g.as_unit('lb').scalar == a.as_unit('lb').scalar


def test_basic_cmp():
    assert V(1, 'kg') < V(2, 'kg')
    assert V(1, 'kg') <= V(2, 'kg')
    assert V(2, 'kg') <= V(2, 'kg')
    assert V(2, 'kg') == V(2, 'kg')
    assert V(2, 'kg') >= V(2, 'kg')
    assert V(2, 'kg') > V(1, 'kg')
    assert V(2, 'kg') >= V(1, 'kg')


def test_conversion_cmp():
    assert V(1, 'kg') < V(100, 'lb')
    assert V(1000000, 'g') > V(100, 'lb')


def test_addition():
    assert V(1, 'kg') + V(2, 'kg') == V(3, 'kg')
    assert V(1, 'kg') + V(1, 'lb') > V(1.4, 'kg')


def test_subtraction():
    assert V(2, 'kg') - V(1, 'kg') == V(1, 'kg')
    assert V(1, 'kg') - V(1, 'lb') < V(0.55, 'kg')


def test_multiplication():
    assert V(2, 'kg') * 2 == V(4, 'kg')
    assert V(2, 'kg') * V(1, 'kg') == V(2, ['kg', 'kg'])


def test_division():
    assert V(8, 'kg') / 2 == V(4, 'kg')
    assert V(2, 'kg') / V(1, 'kg') == V(2, [])
