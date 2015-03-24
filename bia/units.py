from collections import defaultdict


_UNITS = {
    # mass
    'kg': {'type': 'mass', 'scale': 1.0},
    'lb': {'type': 'mass', 'scale': 2.20462},
    'g':  {'type': 'mass', 'scale': 1000.0},

    # length
    'm':  {'type': 'length', 'scale': 1.0},
    'cm': {'type': 'length', 'scale': 100.0},
    'ft': {'type': 'length', 'scale': 3.28084},

    # time
    's': {'type': 'time', 'scale': 1.0},
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
        if (sorted([_UNITS[u]['type'] for u in self.numerator]) !=
            sorted([_UNITS[u]['type'] for u in other.numerator])):
                raise ConversionError('cannot convert {} to {}')
        if (sorted([_UNITS[u]['type'] for u in self.denominator]) !=
            sorted([_UNITS[u]['type'] for u in other.denominator])):
                raise ConversionError('cannot convert {} to {}')

        # compute factor
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
            return UnitValue(self.scalar, self.unit)

        return UnitValue(self.scalar * self.unit.conversion_factor(unit), unit)

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
        return UnitValue(self.scalar + other.scalar, self.unit)

    def __sub__(self, other):
        if self.unit != other.unit:
            other = other.as_unit(self.unit)
        return UnitValue(self.scalar - other.scalar, self.unit)

    def __mul__(self, other):
        if isinstance(other, UnitValue):
            if self.unit != other.unit:
                other = other.as_unit(self.unit)
            return UnitValue(self.scalar * other.scalar, self.unit * other.unit)
        else:
            return UnitValue(self.scalar * other, self.unit)

    def __div__(self, other):
        if isinstance(other, UnitValue):
            if self.unit != other.unit:
                other = other.as_unit(self.unit)
            return UnitValue(self.scalar / other.scalar, self.unit / other.unit)
        else:
            return UnitValue(self.scalar / other, self.unit)
