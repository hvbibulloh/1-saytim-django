from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView, HitCountMixin

from .models import News, Category
from .forms import ContactForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from news_project.custom_permissions import OnlyLoggedSuperUser, UserPassesTestMixin

def news_list(request):
    # news_list = News.object.all()
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }

    return render(request, "news/news_list.html", context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hitcount_response = HitCountMixin.hit_count(request, hit_count)
    if hitcount_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hitcount_response.hit_counted
        hitcontext['hit_message'] = hitcount_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method =="POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #yangi koment obyectini yaratamiz lekin DB ga saqlamaymz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            #komment egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            #malumotlar vazasiga saqlash
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form':comment_form,
        'comment_count':comment_count
    }

    return render(request, 'news/news_detail.html', context)
#@login_required
# def HomePageView(request):
#     news_list = News.published.all().order_by('-publish_time')[:10]
#     categories = Category.objects.all()
#     local_one = News.published.filter(category__name="Mahalliy").order_by("-publish_time")
#     mahalliy_news = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[1:6]
#     context = {
#         'news_list':news_list,
#         'categories': categories,
#         'local_one': local_one,
#         'mahalliy_news': mahalliy_news
#     }
#
#     return render(request, 'news/index.html', context)


class HomePageViews(LoginRequiredMixin,ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['local_one'] = News.published.filter(category__name="Mahalliy").order_by("-publish_time")
        context['mahalliy_news'] = News.published.all().filter(category__name="Mahalliy").order_by("-publish_time")[1:6]
        context['xorij_news'] = News.published.all().filter(category__name="Xorij").order_by("-publish_time")[1:6]
        context['sport_news'] = News.published.all().filter(category__name="Sport").order_by("-publish_time")[1:6]
        context['texnologiya_newa'] = News.published.all().filter(category__name="Texnologiya").order_by("-publish_time")[1:6]
        return context






# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2> Biz bilan bog'langanigiz uchun tashakkur !")
#     context = {'form':form}
#     return render(request, 'news/contact.html', context)
# funksiya orqali


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self,request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form':form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur! </h2>")
        context = {
            'form': form
        }
        return render(request, 'news/contact.html',context)
def errorPageView(request):
    context = {}

    return render(request, 'news/404.html', context)

class MahalliyView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Mahalliy")
        return news

class XorijView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangilikalar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Xorij")
        return news

class TexnologyView(ListView):
    model = News
    template_name = 'news/texno.html'
    context_object_name = 'texno_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Texnologiya")
        return news

class SportView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Sport")
        return news


class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields = ('title', 'body','image', 'category', 'status',)
    template_name = 'cud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = 'cud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateNews(OnlyLoggedSuperUser,CreateView):
    model = News
    template_name = "cud/news_create.html"
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')



@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users

    }

    return render(request, 'pages/admin_page.html', context)


# class SearchResultList(ListView):
#     model = News
#     template_name = 'news/search_result.html'
#     context_object_name = 'barcha_yangiliklar'
#
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)
#                                    )

class SearchResultList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
