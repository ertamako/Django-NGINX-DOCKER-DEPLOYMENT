# Generated by Django 3.0.6 on 2020-07-29 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cnv_app', '0008_auto_20200729_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='TargetBed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('target_bed_document', models.FileField(upload_to='target_bed_files')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('batch_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch')),
            ],
        ),
        migrations.CreateModel(
            name='AntiTargetBed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('anti_target_bed_document', models.FileField(upload_to='antiTarget_bed_files')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('batch_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch')),
            ],
        ),
    ]
