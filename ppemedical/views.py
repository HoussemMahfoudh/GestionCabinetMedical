from django.shortcuts import render
from Article.models import Article
from Service.models import Service


# Create your views here.
def indexView(request):
    articles = Article.objects.all().order_by('-date')[:6]
    services = Service.objects.all()

    context = {
        'articles_instances' : articles,
        'services': services,
    }
    return render(request, 'index.html', context=context)

