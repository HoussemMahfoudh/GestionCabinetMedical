from django.contrib import admin
from Service.models import Service


# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('pk','title','Service_image',)
    list_filter = ('title',)
    search_fields = ('title','content',)


admin.site.register(Service, ServiceAdmin)