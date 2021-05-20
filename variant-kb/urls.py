"""variant_db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('api.urls')),
    path('', views.index, name='index'),
    path('', views.index, name='index'),
    path('genes/', views.genes, name='genes'),
    path('variants/', views.gene, name='variants'),
    path('gene/<str:gene_name>', views.gene, name='gene'),
    path('gene/<str:gene_name>/variant/<str:protein>', views.variant, name='variant'),
    path('gene/<str:gene_name>/variant/<str:protein>/detail', views.variant, name='variant_text'),
    path('', include('side.urls')),
]
