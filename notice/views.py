from django.shortcuts import render
from notice.models import Notice


def main_page(request):
    notice = Notice.objects.all()
    data = {
        'post': notice
    }
    return render(request, 'notice/main.html', data)

