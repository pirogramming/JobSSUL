# Generated by Django 2.1.5 on 2019-02-15 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_merge_20190215_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(default='published', max_length=10),
        ),
    ]
