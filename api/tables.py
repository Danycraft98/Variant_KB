import django_tables2 as tables
from django_tables2.utils import A

from api.models import *

__all__ = [
    'GeneTable', 'GeneCardTable', 'VariantTable', 'VariantCardTable',
    'DiseaseTable', 'DiseaseCardTable', 'HistoryTable'
]


# Gene Table ---------------------------------------------------------------------------------------------------------
class GeneCardTable(tables.Table):
    name = tables.LinkColumn('gene', args=[A('name')], text=lambda record: record.name, empty_values=())
    variants = tables.TemplateColumn('{{ record.variants.count }} variant(s)', verbose_name='Variants')

    class Meta:
        model = Gene
        orderable = False
        fields = sequence = ('name', 'variants')
        attrs = {'class': 'nowrap table table-striped table-hover'}

    @staticmethod
    def class_type():
        return 'Gene'


class GeneTable(GeneCardTable):
    class Meta:
        attrs = {'class': 'dataTable nowrap table table-striped table-hover'}


# Variant Table ------------------------------------------------------------------------------------------------------
class BaseVariantTable(tables.Table):
    variant = tables.LinkColumn('variant_text', args=[A('gene.name'), A('protein')], text=lambda record: record.protein, empty_values=())
    diseases = tables.TemplateColumn('{{ record.diseases.count }} disease(s)', verbose_name='Diseases')

    class Meta:
        abstract = True
        model = Variant
        exclude = (
            'id', 'genome_build', 'consequence', 'exonic_function', 'content', 'germline_content', 'af',
            'af_popmax', 'cosmic70', 'clinvar', 'insilicodamaging', 'insilicobenign', 'polyphen2_hdiv_pred',
            'polyphen2_hvar_pred', 'sift_pred', 'mutationtaster_pred', 'mutationassessor_pred', 'provean_pred',
            'lrt_pred', 'tcga', 'oncokb', 'oncokb_pmids', 'watson', 'watson_pmids', 'qci', 'qci_pmids',
            'jaxckb', 'jaxckb_pmids', 'pmkb', 'pmkb_citations', 'civic', 'google', 'alamut'
        )
        orderable = True
        row_attrs = {
            'title': lambda record: '\n'.join([disease.name + ': [' + disease.get_reviewed_display() + ', ' + disease.branch.upper() + ']' for disease in record.diseases.all()])
            if record.diseases.count() > 0 else 'No Disease'
        }

    @staticmethod
    def class_type():
        return 'Variant'


class VariantTable(BaseVariantTable):
    # edit = tables.LinkColumn('variant', args=[A('gene__name'), A('protein')], text='edit', empty_values=())
    history = tables.TemplateColumn('{{ record.history.first.timestamp }}', verbose_name='Upload Date')
    recent = tables.TemplateColumn('{{ record.history.last.timestamp }}', verbose_name='Last Modified Date')

    class Meta:
        fields = sequence = (
            'variant', 'gene', 'cdna', 'protein', 'transcript', 'chr',
            'start', 'end', 'ref', 'alt', 'diseases', 'history', 'recent'
        )
        attrs = {'class': 'dataTable nowrap table table-striped table-hover'}


class VariantCardTable(BaseVariantTable):
    class Meta:
        fields = sequence = ('variant', 'gene', 'diseases')
        exclude = ('id', 'chr', 'cdna', 'transcript', 'start', 'end', 'alt', 'ref', 'protein')
        attrs = {'class': 'table table-striped table-hover'}


# Disease Table ------------------------------------------------------------------------------------------------------
class BaseDiseaseTable(tables.Table):
    evidences = tables.TemplateColumn('{{ record.evidences.count }} evidence(s)', verbose_name='Evidences')

    class Meta:
        abstract = True
        model = Disease
        orderable = False

    @staticmethod
    def class_type():
        return 'Disease'


class DiseaseCardTable(BaseDiseaseTable):
    class Meta:
        fields = sequence = ('name', 'branch', 'variant', 'evidences')
        exclude = (
            'id', 'others', 'report', 'reviewed_date', 'review_user', 'meta_reviewed_date',
            'meta_review_user', 'approved_date', 'approve_user', 'curation_notes'
        )
        attrs = {
            'class': 'table table-striped table-hover',
            'style': 'display: block; overflow: auto;'
        }


class DiseaseTable(BaseDiseaseTable):
    disease = tables.CheckBoxColumn(checked=True, accessor='name', attrs={'th__input': {'checked': 'checked', 'id': 'selectAll'}})
    functionals = tables.TemplateColumn('{{ record.functionals.count }} functional(s)', verbose_name='Functionals')

    class Meta:
        fields = sequence = ('disease', 'name', 'functionals', 'evidences')
        attrs = {
            'class': 'nowrap table table-striped table-hover',
            'style': 'display: block; overflow: auto;'
        }


# ----------------------------------------------------------------------------------------------------------------
class HistoryTable(tables.Table):
    class Meta:
        model = History
        orderable = False
        order_by = '-timestamp'
        fields = sequence = ('timestamp', 'object', 'content', 'user')
        attrs = {'class': 'nowrap table table-striped table-hover'}
