# Generated by Django 3.0.6 on 2020-09-04 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnv_app', '0031_auto_20200904_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='reference_document',
            field=models.FileField(upload_to='CNVKit/Reference_files'),
        ),
    ]
