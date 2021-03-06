# Generated by Django 3.0.6 on 2020-08-09 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnv_app', '0024_auto_20200808_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='antitargetbed',
            name='r_b_m_b',
            field=models.IntegerField(default=100000, null=True),
        ),
        migrations.AddField(
            model_name='antitargetcoverage',
            name='count',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='antitargetcoverage',
            name='min_mapq',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='targetbed',
            name='r_b_m_b',
            field=models.IntegerField(default=100000, null=True),
        ),
        migrations.AddField(
            model_name='targetcoverage',
            name='count',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='targetcoverage',
            name='min_mapq',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
