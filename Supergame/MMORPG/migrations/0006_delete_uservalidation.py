# Generated by Django 4.0.3 on 2022-04-10 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MMORPG', '0005_uservalidation_isvalidated_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserValidation',
        ),
    ]
