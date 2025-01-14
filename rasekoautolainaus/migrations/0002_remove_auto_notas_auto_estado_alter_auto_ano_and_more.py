# Generated by Django 5.1.4 on 2024-12-09 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasekoautolainaus', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auto',
            name='notas',
        ),
        migrations.AddField(
            model_name='auto',
            name='estado',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='auto',
            name='ano',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='auto',
            name='color',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='auto',
            name='kilometraje',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='auto',
            name='marca',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='auto',
            name='modelo',
            field=models.CharField(max_length=100),
        ),
    ]
