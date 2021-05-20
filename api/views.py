from rest_framework import viewsets, generics

from .serializers import *
from .models import Gene, Variant


class BaseViewSet(viewsets.ModelViewSet):
    base_class = None

    def get_queryset(self):
        queryset = self.base_class.objects.all()
        name = self.kwargs.get('name', None)
        if name and self.base_class:
            queryset = queryset.filter(name=name) if self.base_class != Variant else queryset.filter(protein=name)
        return queryset


class GeneViewSet(BaseViewSet):
    base_class = Gene
    queryset = Gene.objects.all().order_by('name')
    serializer_class = GeneSerializer


class VariantViewSet(BaseViewSet):
    base_class = Variant
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer


class DiseaseViewSet(BaseViewSet):
    base_class = Disease
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
