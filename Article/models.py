from Article.utils import unique_slug_generator, unique_slug_generator_article
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from taggit.models import Tag
from django.db.models.signals import pre_save


class CategorieArticle(models.Model):

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):   
        return reverse("Article:filter-categorie", kwargs={'slug':self.slug})

def slug_generator(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=CategorieArticle)
    

class Article(models.Model):

    class Meta:
        ordering = ['-date']

    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=200,null=True, blank=True)
    categorie = models.ForeignKey(CategorieArticle, on_delete=models.CASCADE)
    image = models.ImageField(max_length=1000)
    content = RichTextUploadingField()
    tags = TaggableManager()
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #template_name = 'Article/ArticleDetailView.html'
        return reverse('Article:detail-article', kwargs={'slug': self.slug})

    def get_related_posts_by_tags(self):
        return Article.objects.filter(tags__in=self.tags.all())
    
    def get_tag_names(self):
        tags = Tag.objects.filter(article__pk=self.pk)
        tags = tags.distinct()
        return tags
        
def slug_generator_article(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)
            
pre_save.connect(slug_generator_article, sender=Article)
    
    
