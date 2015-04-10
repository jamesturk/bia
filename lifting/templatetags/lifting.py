from django import template
from django.template.defaultfilters import stringfilter
from common import to_lb

register = template.Library()


class MassNode(template.Node):
    def __init__(self, weight):
        self.weight = template.Variable(weight)

    def render(self, context):
        try:
            weight_kg = self.weight.resolve(context)
            if context['user'].lifting_options.lifting_units == 'i':
                return to_lb(weight_kg)
            else:
                return remove_exponent(weight_kg)
        except template.VariableDoesNotExist:
            return ''

class MassLabelNode(template.Node):
    def render(self, context):
        return {'i': 'lb', 'm': 'kg'}[context['user'].lifting_options.lifting_units]


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
