from django.contrib import admin
from Materiels.models import Categorie, Materiel

# Register your models here.

class CategorieAdmin(admin.ModelAdmin):
    list_display = ('id','categorie_name',)
    list_filter = ('categorie_name',)
    search_fields = ('categorie_name',)

class MaterielAdmin(admin.ModelAdmin):
    list_display = ('id','title','categorie','Materiel_ref','image','date_ajout',)
    list_filter = ('title','categorie','Materiel_ref')
    search_fields = ('title','categorie','Materiel_ref','description',)

admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Materiel, MaterielAdmin)