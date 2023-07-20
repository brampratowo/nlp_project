from django.contrib import admin
from .models import BiodataPegawai,KategoriPegawai,StatusPegawai

class PegawaiAdmin(admin.ModelAdmin):
    #display fields in add and update form
    list_display=["nip","nama","nik","tempat_lahir","tanggal_lahir","telepon","alamat","kategori","status","agama","foto_identitas"]

    #not display in add and update form
    exclude=["nip","date_deleted","date_updated","created_by","updated_by","deleted_by"]

    #readonly fields
    readonly_fields=["nip_method"]
    
    #filter, search, and edit in list form
    list_filter = ['kategori', 'status']
    search_fields = ['nip', 'nama']
    list_editable = ['status','kategori','agama']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.nip = self.nip_method("")
        else:
            obj.updated_by = request.user.username
        obj.save()
    
    def get_changeform_initial_data(self, request):
        initial_data = super(PegawaiAdmin, self).get_changeform_initial_data(request)
        initial_data['nip'] = int(BiodataPegawai.objects.all().values_list('nip', flat=True).first()) + 1
        return initial_data
    
    def nip_method(self, obj):
        # print(obj.nip)
        if not obj:
            return int(BiodataPegawai.objects.all().values_list('nip', flat=True).order_by('-nip').first()) + 1
        else:
            return obj.nip
    nip_method.short_description = 'Nomor Induk Pegawai'
        
    
class KategoriPegawaiAdmin(admin.ModelAdmin):
    list_display=["kode","nama_kategori"]
    
class StatusPegawaiAdmin(admin.ModelAdmin):
    list_display=["kode","nama_status"]

# Register your models here.
admin.site.register(BiodataPegawai, PegawaiAdmin)
admin.site.register(KategoriPegawai, KategoriPegawaiAdmin)
admin.site.register(StatusPegawai, StatusPegawaiAdmin)