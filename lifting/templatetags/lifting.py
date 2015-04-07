import decimal
from django import template
from django.template.defaultfilters import stringfilter
from lifting.utils import round_to

register = template.Library()

def remove_exponent(d):
    return d.quantize(decimal.Decimal(1)) if d == d.to_integral() else d.normalize()


class MassNode(template.Node):
    def __init__(self, weight):
        self.weight = template.Variable(weight)

    def render(self, context):
        try:
            weight_kg = self.weight.resolve(context)
            if context['user'].profile.lifting_units == 'i':
                return remove_exponent(round_to(weight_kg * decimal.Decimal("2.2046"),
                                                decimal.Decimal("0.125")))
            else:
                return remove_exponent(weight_kg)
        except template.VariableDoesNotExist:
            return ''

class MassLabelNode(template.Node):
    def render(self, context):
        return {'i': 'lbs', 'm': 'kg'}[context['user'].profile.lifting_units]


@register.tag
def mass_unit(parser, token):
    try:
        tag_name, weight = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "{!r} tag requires exactly one argument".format(tag_name)
        )
    return MassNode(weight)


@register.tag
def mass_label(parser, token):
    return MassLabelNode()
