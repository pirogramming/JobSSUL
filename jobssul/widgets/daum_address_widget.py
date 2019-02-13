from django import forms
from django.template.loader import render_to_string
from django.conf import settings


class DaumAddressWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = render_to_string('address_widget.html', {})
        return html

