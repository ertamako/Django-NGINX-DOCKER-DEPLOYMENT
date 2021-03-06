# Generated by Django 3.0.6 on 2020-07-29 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cnv_app', '0007_auto_20200719_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagram',
            name='bam_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cnv_app.BamFile'),
        ),
        migrations.AddField(
            model_name='heatmap',
            name='bam_files',
            field=models.ManyToManyField(blank=True, null=True, to='cnv_app.BamFile'),
        ),
        migrations.AddField(
            model_name='reference',
            name='bam_files',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='cnv_app.BamFile'),
        ),
        migrations.AddField(
            model_name='reference',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scatter',
            name='bam_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cnv_app.BamFile'),
        ),
        migrations.AlterField(
            model_name='antitargetcoverage',
            name='batch_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
        migrations.AlterField(
            model_name='copynumberratio',
            name='batch_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
        migrations.AlterField(
            model_name='copynumbersegment',
            name='batch_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
        migrations.AlterField(
            model_name='targetcoverage',
            name='batch_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
    ]
