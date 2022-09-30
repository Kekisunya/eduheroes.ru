from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import News, NewsCategory, PostViews
from .forms import NewsCreateForm


class NewsHome (ListView):
    model = News
    context_object_name = 'news'
    queryset = News.objects.filter(published=True)
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class NewsByCategory(NewsHome):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = NewsCategory.objects.get(pk=self.kwargs['category_id']).title
        return context

    def get_queryset(self):
        query = News.objects.filter(published=True).filter(categories__pk=self.kwargs['category_id'])
        return query


class NewsByAuthor(NewsHome):
    template_name = 'news/news_my.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) | {
            'title': 'Мои статьи'
        }
        return context

    def get_queryset(self):
        query = News.objects.filter(authors=self.request.user)
        return query


class NewsDetailed(DetailView):
    model = News
    context_object_name = 'item'

    def get(self, request, *args, **kwargs):
        ip = get_user_ip(request)
        news = self.get_object()
        if PostViews.objects.filter(ip=ip).exists():
            news.views.add(PostViews.objects.get(ip=ip))
        else:
            PostViews.objects.create(ip=ip)
            news.views.add(PostViews.objects.get(ip=ip))
        return super().get(request, *args, **kwargs)



class NewsCreate(CreateView):
    form_class = NewsCreateForm
    template_name = 'news/news_add.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs




class NewsEdit(PermissionRequiredMixin, UpdateView):
    model = News
    form_class = NewsCreateForm
    template_name = 'news/news_add.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data() | {
            'view': 'edit',
            'title': 'Редакция статьи',
            'object': self.get_object().id
        }
        return context

    def has_permission(self):
        if self.request.user in News.objects.get(pk=self.kwargs['pk']).authors.all():
            return True
        return False


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('news_by_author')

    def has_permission(self):
        if self.request.user in News.objects.get(pk=self.kwargs['pk']).authors.all():
            return True
        return False


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip





