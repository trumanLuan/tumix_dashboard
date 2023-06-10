from django.db import models

# Create your models here.
# model used in demo.
class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    office = models.CharField(max_length=150)
    age = models.IntegerField()
    start_date = models.DateField()
    salary = models.IntegerField()

    def __str__(self):
        return self.name + " " + self.position + " " + str(self.salary)


# model for study meta-table.
class Study(models.Model):
    id = models.AutoField(primary_key=True)
    dataset = models.CharField(max_length=150)
    species = models.CharField(max_length=150)
    tumor_site = models.CharField(max_length=150)
    biosample_source = models.CharField(max_length=150)
    ndonor = models.IntegerField()
    nsample = models.IntegerField()
    ncell = models.IntegerField()
    nmalignant = models.IntegerField()
    cell_sorting = models.CharField(max_length=150)
    treatment = models.CharField(max_length=150)
    study_title = models.CharField(max_length=1500, default="Default")
    study_geo = models.CharField(max_length=150, default="Default")
    study_pmid = models.CharField(max_length=20, default="Default")

    def __str__(self):
        return self.index

# # model for Sample table.
class Sample(models.Model):
    id = models.AutoField(primary_key=True)


# model for SingleCell.
class SingleCell(models.Model):
    id = models.AutoField(primary_key=True)
    dataset = models.CharField(max_length=150)
    donor = models.CharField(max_length=150)
    sample = models.CharField(max_length=150)
    cell_barcode = models.CharField(max_length=150)
    ncount_rna = models.IntegerField()
    nfeature_rna = models.IntegerField()
    seurat_cluster = models.IntegerField()
    singler_celltype = models.CharField(max_length=150)
    final_major_celltype = models.CharField(max_length=150)

    def __str__(self):
        return self.dataset


# model for Diff_marker_subcluster table.
class Marker_Subcluster(models.Model):
    id = models.AutoField(primary_key=True)
    dataset = models.CharField(max_length=150)
    cluster = models.CharField(max_length=150)
    gene = models.CharField(max_length=150)
    avg_log2FC = models.FloatField()
    pct1 = models.FloatField()
    pct2 = models.FloatField()
    pval = models.FloatField()
    padj = models.FloatField()

    def __str__(self):
        return self.dataset

# model for Diff_marker_celltype table.
class Marker_Celltype(models.Model):
    id = models.AutoField(primary_key=True)
    dataset = models.CharField(max_length=150)
    cluster = models.CharField(max_length=150)
    gene = models.CharField(max_length=150)
    avg_log2FC = models.DecimalField(max_digits=100, decimal_places=4)
    pct1 = models.DecimalField(max_digits=100, decimal_places=4)
    pct2 = models.DecimalField(max_digits=100, decimal_places=4)
    pval = models.DecimalField(max_digits=100, decimal_places=4)
    padj = models.DecimalField(max_digits=100, decimal_places=4)

    def __str__(self):
        return self.dataset

# model for LRpairs.
class LRpairs(models.Model):
    id = models.AutoField(primary_key=True)
    dataset = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    target = models.CharField(max_length=200)
    ligand = models.CharField(max_length=200)
    receptor = models.CharField(max_length=200)
    prob = models.DecimalField(max_digits=100, decimal_places=4)
    pval = models.DecimalField(max_digits=100, decimal_places=4)
    pathway = models.CharField(max_length=200)
    evidence = models.CharField(max_length=200)

    def __str__(self):
        return self.dataset

# model for SignalPathway.
class SignalPathway(models.Model):
    id = models.AutoField(primary_key=True)
    dataset = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    target = models.CharField(max_length=200)
    pathway = models.CharField(max_length=200)
    prob = models.DecimalField(max_digits=100, decimal_places=4)
    pval = models.DecimalField(max_digits=100, decimal_places=4)

    def __str__(self):
        return self.dataset