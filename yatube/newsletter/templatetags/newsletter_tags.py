from django import template
from newsletter.forms import NewsletterForm

register = template.Library()


@register.inclusion_tag("newsletter/tags/form.html")
def newsletter_form():
    return {'newsletter_form': NewsletterForm()}
