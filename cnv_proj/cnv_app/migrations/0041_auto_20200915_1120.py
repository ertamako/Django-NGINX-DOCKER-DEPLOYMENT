# Generated by Django 3.0.6 on 2020-09-15 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnv_app', '0040_auto_20200914_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bamfile',
            name='bam_document',
            field=models.FileField(upload_to=''),
        ),
    ]
