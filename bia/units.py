from collections import defaultdict


class UnitError(ValueError):
    pass


class ConversionError(ValueError):
    pass


class Unit(object):
    _mapping = {}

    def __init__(self, n, unit):
        self.scalar = n
        if unit not in self._mapping:
            raise ValueError('invalid unit {} for {}'.format(unit, self.__class__.__name__))
        self.unit = unit

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

    def __cmp__(self):
        pass


class Mass(Unit):
    _base = 'kg'

    # 1kg ==
    _mapping = {
        'kg': 1.0,
        'lb': 2.20462,
        'g': 1000.0,
    }
