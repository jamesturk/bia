import decimal
from django import template
from django.template.defaultfilters import stringfilter
from lifting.utils import round_to

register = template.Library()


class MassNode(template.Node):
    def __init__(self, weight):
        self.weight = template.Variable(weight)

    def render(self, context):
        try:
            weight_kg = self.weight.resolve(context)
            return round_to(weight_kg * decimal.Decimal("2.2046"), decimal.Decimal("0.125"))
        except template.VariableDoesNotExist:
            return ''


@register.tag
def mass_unit(parser, token):
    try:
        tag_name, weight = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "{!r} tag requires exactly one argument".format(tag_name)
        )
    return MassNode(weight)
