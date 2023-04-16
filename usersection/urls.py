from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('user-profile/',login_required(UserProfileUpdateView.as_view()),name="UserProfileUpdateView"),
    path('article/<int:id>/',showSingleArticle,name="ShowSingleArticle"),
    path('search/',articleSearchView,name="SearchArticle"),
    path('user-articles/',userAllArticles,name="UserAllArticles"),
]
