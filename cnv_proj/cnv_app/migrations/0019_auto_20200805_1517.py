# Generated by Django 3.0.6 on 2020-08-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnv_app', '0018_auto_20200805_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagram',
            name='document',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='heatmap',
            name='document',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='scatter',
            name='document',
            field=models.ImageField(upload_to=''),
        ),
    ]
