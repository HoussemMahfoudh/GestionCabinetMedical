from django.contrib import admin
from Article.models import Article, CategorieArticle

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','categorie','image','tags','date','updated')
    list_filter = ('title','categorie','tags','date',)
    search_fields = ('title','content','categorie','tags','date',)

class CategorieArticleAdmin(admin.ModelAdmin):
    list_display = ('pk','title','slug',)
    list_filter = ('title',)
    search_fields = ('title',)



admin.site.register(Article, ArticleAdmin)
admin.site.register(CategorieArticle, CategorieArticleAdmin)