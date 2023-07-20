from django.db import models

class AbstractModel(models.Model):
    date_deleted = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50,null=True, blank=True)
    updated_by = models.CharField(max_length=50,null=True, blank=True)
    deleted_by = models.CharField(max_length=50,null=True, blank=True)

    class Meta:
        abstract = True

class Agama(models.Model):
    kode = models.CharField(max_length=5, unique=True)
    nama_agama = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nama_agama
    
    class Meta:
        verbose_name = "Data Agama"
        verbose_name_plural = "List Data Agama"