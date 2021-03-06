import pytest
from .units import Unit, ConversionError
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


def test_complex_conversions():
    a = V(2, ['m', 'm'])
    cm2 = a.as_unit(['cm', 'cm'])
    assert cm2.scalar == 20000
    assert cm2.unit == Unit(['cm', 'cm'])

    g = V(9.8, Unit(['m'], ['s', 's']))
    g_ft = g.as_unit(Unit(['ft'], ['s', 's']))
    assert g_ft.scalar - 32 < 1
    assert g_ft.unit == Unit(['ft'], ['s', 's'])


def test_invalid_conversion_basic():
    with pytest.raises(ConversionError):
        V(1, 'm').as_unit('s')


def test_invalid_conversion_dimension():
    with pytest.raises(ConversionError):
        V(1, ['m']).as_unit(['m', 'm'])


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
