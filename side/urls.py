from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('search/', views.search, name='search'),
    path('gene/<str:gene_name>/variant/<str:protein>/export', views.export, name='export'),
    path('gene/<str:gene_name>/variant/<str:protein>/exported', views.exported, name='exported'),
    path('gene/<str:gene_name>/variant/<str:protein>/history', views.history, name='history'),
]
