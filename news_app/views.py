from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from .models import News, Category
from .forms import ContactForm

def news_list(request):
    # news_list = News.object.all()
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }

    return render(request, "news/news_list.html", context)

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        "news": news
    }

    return render(request, 'news/news_detail.html', context)

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


class HomePageViews(ListView):
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