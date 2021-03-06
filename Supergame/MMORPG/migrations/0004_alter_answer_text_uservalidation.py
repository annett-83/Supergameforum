# Generated by Django 4.0.3 on 2022-04-10 01:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MMORPG', '0003_remove_answer_accept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(max_length=256),
        ),
        migrations.CreateModel(
            name='UserValidation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='UserValidation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
