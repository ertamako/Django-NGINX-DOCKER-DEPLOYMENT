# Generated by Django 3.0.6 on 2020-08-07 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cnv_app', '0022_auto_20200807_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
