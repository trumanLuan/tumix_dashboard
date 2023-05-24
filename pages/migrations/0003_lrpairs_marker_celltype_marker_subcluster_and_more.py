# Generated by Django 4.2 on 2023-05-24 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_study'),
    ]

    operations = [
        migrations.CreateModel(
            name='LRpairs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=200)),
                ('target', models.CharField(max_length=200)),
                ('ligand', models.CharField(max_length=200)),
                ('receptor', models.CharField(max_length=200)),
                ('prob', models.DecimalField(decimal_places=4, max_digits=100)),
                ('pval', models.DecimalField(decimal_places=4, max_digits=100)),
                ('pathway', models.CharField(max_length=200)),
                ('evidence', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Marker_Celltype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset', models.CharField(max_length=150)),
                ('cluster', models.CharField(max_length=150)),
                ('gene', models.CharField(max_length=150)),
                ('avg_log2FC', models.DecimalField(decimal_places=4, max_digits=100)),
                ('pct1', models.DecimalField(decimal_places=4, max_digits=100)),
                ('pct2', models.DecimalField(decimal_places=4, max_digits=100)),
                ('pval', models.DecimalField(decimal_places=4, max_digits=100)),
                ('padj', models.DecimalField(decimal_places=4, max_digits=100)),
            ],
        ),
        migrations.CreateModel(
            name='Marker_Subcluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset', models.CharField(max_length=150)),
                ('cluster', models.CharField(max_length=150)),
                ('gene', models.CharField(max_length=150)),
                ('avg_log2FC', models.FloatField()),
                ('pct1', models.FloatField()),
                ('pct2', models.FloatField()),
                ('pval', models.FloatField()),
                ('padj', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SignalPathway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=200)),
                ('target', models.CharField(max_length=200)),
                ('pathway', models.CharField(max_length=200)),
                ('prob', models.DecimalField(decimal_places=4, max_digits=100)),
                ('pval', models.DecimalField(decimal_places=4, max_digits=100)),
            ],
        ),
        migrations.CreateModel(
            name='SingleCell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset', models.CharField(max_length=150)),
                ('donor', models.CharField(max_length=150)),
                ('sample', models.CharField(max_length=150)),
                ('cell_barcode', models.CharField(max_length=150)),
                ('ncount_rna', models.IntegerField()),
                ('nfeature_rna', models.IntegerField()),
                ('seurat_cluster', models.IntegerField()),
                ('singler_celltype', models.CharField(max_length=150)),
                ('final_major_celltype', models.CharField(max_length=150)),
            ],
        ),
    ]
