# Generated by Django 4.0 on 2023-09-04 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0004_alter_news_managers_news_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
    ]