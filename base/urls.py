
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('company.urls')),
    path('', include('industry.urls')),
    path('', include('watchlist.urls')),
    path('', include('article.urls')),

    path("__reload__/", include("django_browser_reload.urls")),

    # The catch-all route
    # path('<str:slug>/', TemplateView.as_view(template_name='404.html'), name='404'),
]
handler404 = TemplateView.as_view(template_name='404.html')