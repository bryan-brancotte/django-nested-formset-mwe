import logging

from django import template
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def as_bootstrap_alert(o):
    ret = []
    if isinstance(o, ErrorList):
        for error in o:
            ret.append("""<div class="alert alert-danger">%s</div>""" % error.replace("\n", "<br/>"))
    else:
        ret.append("""<div class="alert alert-danger">Can't bootstrapize object of class %s</div>""" %
                   str(type(object).__name__))
    return mark_safe("".join(ret))
