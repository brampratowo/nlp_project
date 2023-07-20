from django.contrib import admin
from .models import Upload

class MemberUpload(admin.ModelAdmin):
    list_display=["image","action","updated","created"]
# Register your models here.
admin.site.register(Upload, MemberUpload)
