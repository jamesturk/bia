from collections import defaultdict


_UNITS = {
    # mass
    'kg': {'base': 'kg', 'scale': 1.0},
    'lb': {'base': 'kg', 'scale': 2.20462},
    'g':  {'base': 'kg', 'scale': 1000.0},

    'm':  {'base': 'm', 'scale': 1.0},
    'cm': {'base': 'm', 'scale': 100.0},
    'ft': {'base': 'm', 'scale': 3.28084},

    's': {'base': 's', 'scale': 1.0},
}


class UnitError(ValueError):
    pass


class ConversionError(ValueError):
    pass


class Unit(object):
    def __init__(self, numerator, denominator=None):
        if isinstance(numerator, str):
            self.numerator = [numerator]
        else:
            self.numerator = numerator
        self.denominator = [] if denominator is None else denominator
        for u in self.numerator + self.denominator:
            if u not in _UNITS:
                raise ValueError('invalid unit {}'.format(self))

        self._simplify()

    def __str__(self):
        return '*'.join(self.numerator)

    def __repr__(self):
        return 'Unit({!r}, {!r})'.format(self.numerator, self.denominator)

    def __eq__(self, other):
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __mul__(self, other):
        return Unit(self.numerator + other.numerator, self.denominator + other.denominator)

    def __div__(self, other):
        return Unit(self.numerator + other.denominator, self.denominator + other.numerator)

    def _simplify(self):
        for u in list(self.denominator):
            if u in self.numerator:
                self.numerator.remove(u)
                self.denominator.remove(u)

    def conversion_factor(self, other):
        factor = 1
        for u in self.numerator:
            factor /= _UNITS[u]['scale']
        for u in other.numerator:
            factor *= _UNITS[u]['scale']
        return factor

    @staticmethod
    def unit(u):
        if isinstance(u, Unit):
            return u
        else:
            return Unit(u)


class UnitValue(object):
    def __init__(self, n, unit):
        self.scalar = float(n)
        self.unit = Unit.unit(unit)

    def as_unit(self, unit):
        unit = Unit.unit(unit)
        if self.unit == unit:
            return self.__class__(self.scalar, self.unit)

        return self.__class__(self.scalar * self.unit.conversion_factor(unit), unit)

    def __str__(self):
        return '{}{}'.format(self.scalar, self.unit)

    def __repr__(self):
        return 'U({}, {!r})'.format(self.scalar, self.unit)

    def __cmp__(self, other):
        if self.unit != other.unit:
            other = other.as_unit(self.unit)
        # cmp() removed in Python 3, recommended to replace with this
        return (self.scalar > other.scalar) - (self.scalar < other.scalar)

    def __add__(self, other):
        if self.unit != other.unit:
            other = other.as_unit(self.unit)
        return self.__class__(self.scalar + other.scalar, self.unit)

    def __sub__(self, other):
        if self.unit != other.unit:
            other = other.as_unit(self.unit)
        return self.__class__(self.scalar - other.scalar, self.unit)

    def __mul__(self, other):
        if isinstance(other, UnitValue):
            if self.unit != other.unit:
                other = other.as_unit(self.unit)
            return self.__class__(self.scalar * other.scalar, self.unit * other.unit)
        else:
            return self.__class__(self.scalar * other, self.unit)

    def __div__(self, other):
        if isinstance(other, UnitValue):
            if self.unit != other.unit:
                other = other.as_unit(self.unit)
            return self.__class__(self.scalar / other.scalar, self.unit / other.unit)
        else:
            return self.__class__(self.scalar / other, self.unit)
