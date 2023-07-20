from django.contrib import admin
from .models import Agama

class MemberAgama(admin.ModelAdmin):
    list_display=["kode","nama_agama"]

# Register your models here.
admin.site.register(Agama, MemberAgama)

