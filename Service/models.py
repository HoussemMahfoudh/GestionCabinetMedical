from django.db import models
from django.urls import reverse
from ppemedical.utils import unique_slug_generator
from django.db.models.signals import pre_save
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Service(models.Model):
    title=models.CharField( max_length=250)
    Service_image=models.ImageField(null=True, blank=True, max_length=1000)
    content = RichTextUploadingField()
    slug =models.SlugField(max_length=250, null=True, blank=True)
    

    def __str__(self):
        return self.title 
    '''
    def get_absolute_url(self):
        return reverse("Service:DetailService", kwargs={"slug": self.slug})
    '''

def slug_generator(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug=unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Service)

