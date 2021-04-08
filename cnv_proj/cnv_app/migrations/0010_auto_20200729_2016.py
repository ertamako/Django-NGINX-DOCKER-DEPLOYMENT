# Generated by Django 3.0.6 on 2020-07-29 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cnv_app', '0009_antitargetbed_targetbed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antitargetbed',
            name='batch_run',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
        migrations.AlterField(
            model_name='antitargetcoverage',
            name='batch_run',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
        migrations.AlterField(
            model_name='copynumberratio',
            name='batch_run',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
        migrations.AlterField(
            model_name='copynumbersegment',
            name='batch_run',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
        migrations.AlterField(
            model_name='diagram',
            name='batch_run',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
        migrations.AlterField(
            model_name='heatmap',
            name='batch_run',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='bam_files',
            field=models.ManyToManyField(default=None, null=True, to='cnv_app.BamFile'),
        ),
        migrations.AlterField(
            model_name='scatter',
            name='batch_run',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
        migrations.AlterField(
            model_name='targetbed',
            name='batch_run',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
        migrations.AlterField(
            model_name='targetcoverage',
            name='batch_run',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cnv_app.Batch'),
        ),
    ]
