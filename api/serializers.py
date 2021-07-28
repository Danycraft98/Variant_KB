from rest_framework import serializers

from .models import Disease, Variant, Gene


class DiseaseSerializer(serializers.ModelSerializer):
    gene = serializers.SerializerMethodField()
    variant = serializers.SerializerMethodField()
    gdr = serializers.SerializerMethodField()
    vdr = serializers.SerializerMethodField()

    @staticmethod
    def get_gene(obj):
        return obj.variant.gene.id

    @staticmethod
    def get_variant(obj):
        return obj.variant.id

    @staticmethod
    def get_gdr(obj):
        report = obj.reports.filter(report_name='Gene-Disease').first()
        if report:
            return report.content
        return ''

    @staticmethod
    def get_vdr(obj):
        report = obj.reports.filter(report_name='Variant-Disease').first()
        if report:
            return report.content
        return ''

    class Meta:
        model = Disease
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
    diseases = DiseaseSerializer(required=False, many=True)

    class Meta:
        model = Variant
        fields = '__all__'


class GeneFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'


class GeneSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(required=False, many=True)
    gene_fields = GeneFieldSerializer(required=False, many=True)

    class Meta:
        model = Gene
        fields = ('name', 'content', 'variants', 'gene_fields')
