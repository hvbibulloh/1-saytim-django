from django.urls import path
from .views import news_list, news_detail, ContactPageView, errorPageView, HomePageViews, MahalliyView, SportView, \
    TexnologyView, XorijView, NewsDeleteView, NewsUpdateView, NewsCreateNews, admin_page, SearchResultList

urlpatterns = [
    path('', HomePageViews.as_view(), name='home_page'),
    path('news/', news_list, name="all_news_list"),
    path('news/create/', NewsCreateNews.as_view(), name="news_create"),
    path('news/<slug:news>/', news_detail, name="news_detail_page"),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('404/', errorPageView, name='error_page'),
    path('mahalliy/', MahalliyView.as_view(), name="mahalliy_news_page"),
    path('texnology/', TexnologyView.as_view(), name="texnology_news_page"),
    path('xorij/', XorijView.as_view(), name="xorij_news_page"),
    path('sport/', SportView.as_view(), name="sport_news_page"),
    path('adminpage/', admin_page, name="admin_page"),
    path('search/', SearchResultList.as_view(), name='search_result'),

]