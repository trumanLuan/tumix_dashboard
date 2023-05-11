from django.db import models

# Create your models here.
# model used in demo.
class Employee(models.Model):
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
    index = models.CharField(max_length=150)
    species = models.CharField(max_length=150)
    tumor_site = models.CharField(max_length=150)
    biosample_source = models.CharField(max_length=150)
    ndonor = models.IntegerField()
    nsample = models.IntegerField()
    ncell = models.IntegerField()
    nmalignant = models.IntegerField()
    cell_sorting = models.CharField(max_length=150)
    treatment = models.CharField(max_length=150)

    def __str__(self):
        return self.index


