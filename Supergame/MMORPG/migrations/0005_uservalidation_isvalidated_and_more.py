# Generated by Django 4.0.3 on 2022-04-10 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MMORPG', '0004_alter_answer_text_uservalidation'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservalidation',
            name='isValidated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='uservalidation',
            name='validationCode',
            field=models.CharField(default='000000', max_length=6),
        ),
    ]
