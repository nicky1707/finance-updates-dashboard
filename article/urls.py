from django.urls import path
from .views import (home, search, feed)


urlpatterns = [
    path('', home, name="home"),
    path('search/', search, name="search"),
    path('<str:watchlist_name>/', feed, name="feed"),
]
