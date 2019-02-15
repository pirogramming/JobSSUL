
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from datetime import timezone
from django.db import models
import django
from django.urls import reverse
from jobssul import settings
from accounts.models import User

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')
#     user_for_related_fields = True
#
#     def published(self, **kwargs):
#         return self.filter(status='published', **kwargs)


class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()
    PAYMENT_LEVEL = (
        ('평범', '7500원 ~ 9000원'),
        ('굳', '9000원 ~ 10500원'),
        ('쏘 굳', '10500원 이상'),
    )


    WORK_TYPE = (
        ('단기', '단기'),
        ('장기', '장기'),
    )

    STATUS_CHOICES = {
        ('draft', 'Draft'),
        ('published', 'Published'),
    }

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, verbose_name= '제목')
    content = models.TextField(verbose_name='내용', validators=[MinLengthValidator(10, message=None)],
                               help_text='내용을 최소 10자 이상으로 작성해주세요')
    payment = models.CharField(max_length=10, choices=PAYMENT_LEVEL, verbose_name='시급')
    workplace = models.CharField(max_length=50, verbose_name='지점')
    recommend = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name = '별점')
    work_type = models.CharField(max_length=10, choices=WORK_TYPE, verbose_name='직종')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    class Meta:
        ordering = ['-id']



    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now = True)

    # def published(self):
    #     now = timezone.now()
    #     return now


    def __str__(self):
        template = '{0.title} {0.author}'
        return template.format(self)

    def edit_post_url(self):
        return reverse('main:edit', args=[self.pk])

    def delete_post_url(self):
        return reverse('main:delete', args=[self.pk])

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('main:detail', args=[self.pk])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reply = models.ForeignKey('Comment', null=True, related_name='replies', on_delete=models.CASCADE)

    def get_edit_url(self):
        return reverse('main:comment_edit', args=[self.pk])

    def get_delete_url(self):
        return reverse('main:comment_delete', args=[self.pk])

    def get_absolute_url(self):
        return reverse('main:detail', args=[self.pk])

