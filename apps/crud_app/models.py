from django.db import models
from apps.crud_app_master.models import AbstractModel
 
# Create your models here.
class BiodataPegawai(AbstractModel):
    nip = models.CharField(max_length = 20, unique=True, verbose_name='NIP')
    nama = models.CharField(max_length = 200)
    nik = models.CharField(max_length = 20)
    tempat_lahir = models.CharField(max_length = 200, null=True, blank=True)
    tanggal_lahir = models.DateField()
    telepon = models.CharField(max_length = 20, null=True, blank=True)
    alamat = models.CharField(max_length = 500, null=True, blank=True)
    kategori = models.ForeignKey('KategoriPegawai', on_delete=models.CASCADE)
    status = models.ForeignKey('StatusPegawai', on_delete=models.CASCADE)
    agama = models.ForeignKey('crud_app_master.Agama', on_delete=models.CASCADE)
    foto_identitas = models.ImageField(upload_to="images/identitas", null=True, blank=True)

    def __str__(self) -> str:
        return self.nama
    
    class Meta:
        verbose_name = "Data Pegawai"
        verbose_name_plural = "List Data Pegawai"

class KategoriPegawai(models.Model):
    kode = models.CharField(max_length=20, unique=True)
    nama_kategori = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nama_kategori
    
    class Meta:
        verbose_name = "Kategori Pegawai"
        verbose_name_plural = "List Kategori Pegawai"

class StatusPegawai(models.Model):
    kode = models.CharField(max_length=20, unique=True)
    nama_status = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nama_status
    
    class Meta:
        verbose_name = "Status Pegawai"
        verbose_name_plural = "List Status Pegawai"
