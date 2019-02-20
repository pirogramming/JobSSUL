from django.shortcuts import render
from claim.models import Claim


def main_page(request):
    claim = Claim.objects.all()
    data = {
        'post': claim
    }
    return render(request, 'claim/main.html', data)

