# Generated by Django 4.0.3 on 2022-04-09 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MMORPG', '0002_subuser_answer_isaccepted_category_subscriber_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='accept',
        ),
    ]