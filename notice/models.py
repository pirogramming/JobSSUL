from django.core.validators import MinLengthValidator
from django.db import models
# from django.urls import reverse
from accounts.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')
#     user_for_related_fields = True
#
#     def published(self, **kwargs):
#         return self.filter(status='published', **kwargs)


class Notice(models.Model):
    objects = models.Manager()
    published = PublishedManager()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, verbose_name= '제목')
    content = models.TextField(verbose_name='내용', validators=[MinLengthValidator(10, message=None)],
                               help_text='내용을 최소 10자 이상으로 작성해주세요')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default='published')

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

    # def edit_post_url(self):
    #     return reverse('notice:edit', args=[self.pk])
    #
    # def delete_post_url(self):
    #     return reverse('notice:delete', args=[self.pk])
    #
    # def get_absolute_url(self):
    #     return reverse('notice:detail', args=[self.pk])

