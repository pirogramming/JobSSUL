from django import forms
from django.template.loader import render_to_string


class DaumAddressWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = render_to_string('address_widget.html', {
        }) #context
        return html


class DaumMapWidget(forms.TextInput):
    def render(self, name, value, attrs, renderer=None):
        html = render_to_string('map_widget.html')
        return html

