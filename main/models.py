from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.
from django.urls import reverse
from jobssul import settings

from accounts.models import User


class Post(models.Model):
    PAYMENT_LEVEL = (
        ('평범', '7500원 ~ 9000원'),
        ('굳', '9000원 ~ 10500원'),
        ('쏘 굳', '10500원 이상'),
    )

    RECOMMEND_LEVEL = (
        ('*', '*'),
        ('**', '**'),
        ('***', '***'),
        ('****', '****'),
        ('*****', '*****'),
    )

    WORK_TYPE = (
        ('단기', '단기'),
        ('장기', '장기'),
    )

    title = models.CharField(max_length=20, verbose_name= '제목')
    content = models.TextField(verbose_name='내용', validators=[MinLengthValidator(200, message=None)],
                               help_text='내용을 최소 200자 이상으로 작성해주세요')
    payment = models.CharField(max_length=10, choices=PAYMENT_LEVEL, verbose_name='시급')
    workplace = models.CharField(max_length=50, verbose_name='지점')
    recommend = models.CharField(max_length=5, choices=RECOMMEND_LEVEL, verbose_name = '별점')
    work_type = models.CharField(max_length=10, choices=WORK_TYPE, verbose_name='직종')

    def __str__(self):
        return self.title




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def get_edit_url(self):
        return reverse('main:comment_edit', args=[self.pk])

    def get_delete_url(self):
        return reverse('main:comment_delete', args=[self.pk])

    def get_absolute_url(self):
        return reverse('main:main_detail', args=[self.pk])
