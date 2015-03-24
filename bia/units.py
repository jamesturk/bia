from collections import defaultdict


class UnitError(ValueError):
    pass


class ConversionError(ValueError):
    pass


class Unit(object):
    _mapping = {}

    def __init__(self, n, unit, denom=None):
        self.scalar = float(n)

        if isinstance(unit, str):
            self.unit_numerator = [unit]
        else:
            self.unit_numerator = unit

        self.unit_denominator = [] if denom is None else denom

        for u in self.unit_numerator + self.unit_denominator:
            if u not in self._mapping:
                raise ValueError('invalid unit {} for {}'.format(unit, self.__class__.__name__))

    @property
    def unit(self):
        return '*'.join(self.unit_numerator)

    def as_unit(self, unit):
        if self.unit == unit:
            return self.__class__(self.scalar, self.unit)

        try:
            if self.unit == self._base:
                factor = self._mapping[unit]
            else:
                factor = self._mapping[unit] / self._mapping[self.unit]
        except KeyError:
            raise ConversionError('cannot convert from {} to {}'.format(self.unit, unit))

        return self.__class__(self.scalar * factor, unit)

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
        if isinstance(other, Unit):
            if self.unit != other.unit:
                other = other.as_unit(self.unit)
            return self.__class__(self.scalar * other.scalar,
                                  self.unit_numerator + other.unit_numerator)
        else:
            return self.__class__(self.scalar * other, self.unit)

    def __div__(self, other):
        if isinstance(other, Unit):
            if self.unit != other.unit:
                other = other.as_unit(self.unit)
            new_numerator = list(self.unit_numerator)
            new_denominator = list(self.unit_denominator)
            for u in other.unit_numerator:
                if u in new_numerator:
                    new_numerator.remove(u)
                else:
                    new_denominator.append(u)

            return self.__class__(self.scalar / other.scalar, new_numerator, new_denominator)
        else:
            return self.__class__(self.scalar / other, self.unit)

class Mass(Unit):
    _base = 'kg'

    # 1kg ==
    _mapping = {
        'kg': 1.0,
        'lb': 2.20462,
        'g': 1000.0,
    }
