# Generated by Django 4.2.3 on 2023-07-18 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_rename_index_study_dataset'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneExpr',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dataset', models.CharField(max_length=200)),
                ('cluster', models.CharField(max_length=150)),
                ('gene', models.CharField(max_length=200)),
                ('expr_ratio', models.DecimalField(decimal_places=4, max_digits=100)),
                ('expr_mean', models.DecimalField(decimal_places=4, max_digits=100)),
                ('expr_median', models.DecimalField(decimal_places=4, max_digits=100)),
            ],
        ),
        migrations.CreateModel(
            name='GeneExprCorr',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dataset', models.CharField(max_length=200)),
                ('gene1', models.CharField(max_length=200)),
                ('gene2', models.CharField(max_length=200)),
                ('corr', models.DecimalField(decimal_places=4, max_digits=100)),
                ('cluster', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]