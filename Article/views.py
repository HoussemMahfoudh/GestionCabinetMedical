from django.shortcuts import render
from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.detail import DetailView, SingleObjectMixin
from Article.models import Article, CategorieArticle
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Count
from taggit.models import Tag

class CategorieListView(ListView):

    model = Article
    template_name = 'Article/ArticleListView.html'

    def get_queryset(self):
        self.categorie = get_object_or_404(CategorieArticle, slug=self.kwargs['slug'])
        return Article.objects.filter(categorie=self.categorie)

    def get_context_data(self, **kwargs):
        context = super(CategorieListView, self).get_context_data(**kwargs)
        context['categories'] = CategorieArticle.objects.annotate(total=Count('article'))
        context['articles'] = Article.objects.filter(categorie=self.categorie)
        context['tags'] = Tag.objects.all()
        return context
    

class ArticleListView(ListView):

    model = Article
    context_object_name = 'articles'
    template_name = 'Article/ArticleListView.html'
    paginate_by = 4

    def get_queryset(self):
        return Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['categories'] = CategorieArticle.objects.annotate(total=Count('article'))
        context['tags'] = Tag.objects.all()
        return context
    

class ArticleDetailView(DetailView):

    model = Article
    template_name = 'Article/ArticleDetailView.html'
    
    #similar_posts = instance.tags.similar_objects()
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article = super(ArticleDetailView, self).get_object(queryset=None)
        article_related = article.tags.similar_objects()
        context['categories'] = CategorieArticle.objects.annotate(total=Count('article'))
        context['article_related'] = article_related
        context['tags'] = Tag.objects.all()
        return context
    
    


def search(request):
    template = 'Article/ArticleListView.html'
    if 'q' in request.GET:
        query = request.GET.get('q')
        articles = Article.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        context = {
            'articles':articles,
            'categories':CategorieArticle.objects.annotate(total=Count('article')),
            'tags': Tag.objects.all(),
        }
        return render(request, template, context)
    else:
        raise ValueError("erreur!")


