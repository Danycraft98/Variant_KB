import django_tables2 as tables

from api.models import *

__all__ = ['DiseaseTable', 'HistoryTable']


class DiseaseTable(tables.Table):
    disease = tables.CheckBoxColumn(checked=True, accessor='name', attrs={'th__input': {'checked': 'checked', 'id': 'selectAll'}})
    functionals = tables.TemplateColumn('{{ record.functionals.count }} functional(s)', verbose_name='Functionals')
    evidences = tables.TemplateColumn('{{ record.evidences.count }} evidence(s)', verbose_name='Evidences')

    class Meta:
        model = Disease
        orderable = False
        sequence = ('disease', 'name', 'functionals', 'evidences')
        exclude = ('id', 'report', 'variant', 'curation_notes', 'reviewed_date', 'meta_reviewed_date', 'approved_date')
        attrs = {
            'class': 'nowrap table table-striped table-hover',
            'style': 'display: block; overflow: auto;'
        }

    @staticmethod
    def class_type():
        return 'Disease'


class HistoryTable(tables.Table):
    class Meta:
        model = History
        orderable = False
        order_by = '-timestamp'
        sequence = ('timestamp', 'object', 'content', 'user')
        exclude = ('id', 'variant')
        attrs = {'class': 'nowrap table table-striped table-hover'}
