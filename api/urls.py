from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'genes(?:/(?P<name>.*))?', views.GeneViewSet)
router.register(r'variants(?:/(?P<name>.*))?', views.VariantViewSet)
router.register(r'diseases(?:/(?P<name>.*))?', views.DiseaseViewSet)


urlpatterns = [
    path('api/', include((router.urls, 'variant-kb'), namespace='api'), name='api'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
