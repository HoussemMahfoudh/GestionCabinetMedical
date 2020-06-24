from django.db import models
from django.urls import reverse
from ppemedical.utils import unique_slug_generator
from django.db.models.signals import pre_save
from datetime import datetime, date
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Categorie(models.Model):
    categorie_name=models.CharField(max_length=1000)
    
    #covert object to string
    def __str__(self):
        return self.categorie_name 

    
class Materiel(models.Model):
    categorie=models.ForeignKey(Categorie, on_delete=models.CASCADE)
    title=models.CharField( max_length=250)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    Materiel_ref=models.IntegerField(default=0)
    image=models.ImageField(null=True, blank=True, max_length=1000)
    description=RichTextUploadingField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    #covert object to string
    def __str__(self):
        return self.title
    
    #permet de reenvoie l'URL
    def get_absolute_url(self):
        return reverse("Materiel:detailMateriels", kwargs={"slug": self.slug})

def slug_generator(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug=unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Materiel)


#-----------------------------------------------------------#
