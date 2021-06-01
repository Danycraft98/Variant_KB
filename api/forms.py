from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import modelformset_factory, BaseModelFormSet, model_to_dict

from .constants import REVIEWED_CHOICES, FUNC_CAT_CHOICES, GP_DX_CHOICES, SO_DX_CHOICES
from .models import *


# Base Forms------------------------------------------------------------------------------------------------------
class BaseCustomModelFormSet(BaseModelFormSet):
    def add_fields(self, form, index):
        super(BaseCustomModelFormSet, self).add_fields(form, index)
        self.set_nested(form, {}, index)

    def is_valid(self):
        result = super(BaseCustomModelFormSet, self).is_valid()
        for form in self.forms:
            if hasattr(form, 'nested'):
                result = result and any(sub_form.is_valid() for sub_form in form.nested) if type(form.nested) == list \
                    else result and form.nested.is_valid()
        return result

    def save(self, commit=True):
        result = super(BaseCustomModelFormSet, self).save(commit=commit)
        for form in self.forms:
            if hasattr(form, 'nested') and not self._should_delete_form(form):
                [sub_form.save(commit=commit) for sub_form in form.nested]
        return result

    def set_nested(self, form, formsets_info, index):
        form.nested = []
        for formset, info in formsets_info.items():
            query = self.set_query(info[1], index)
            query = query.filter(~Q(item='')).all() if 'func' in info[0] else\
                (query.filter(item='').all() if 'act' in info[0] else query)
            try:
                init = query.values() if info[1] != Score else query
            except Score.DoesNotExist:
                init = []
            formset_dict = {
                'initial': init, 'data': form.data if form.is_bound else None,
                'files': form.files if form.is_bound else None, 'prefix': info[0] % form.prefix,
            }
            if info[1] in [Evidence, Report]:
                formset_dict.pop('initial')
                formset_dict['queryset'] = query
            form.nested.append(formset(**formset_dict))

    def set_query(self, class_name, index):
        return self.get_queryset()[index] if index is not None and len(self.get_queryset()) > index else class_name.objects.none().first()

    def get_forms(self):
        form_list = [self]
        for form in self.forms:
            if hasattr(form, 'nested'):
                sub_forms = form.nested
                for sub_form in sub_forms:
                    form_list.append(sub_form)
                    form_list.extend(sub_form.get_forms()) if hasattr(sub_form, 'get_forms') else None
        return form_list


class DiseaseForm(forms.ModelForm):
    name = forms.ChoiceField(choices=GP_DX_CHOICES, widget=forms.Select(attrs={'placeholder': 'Disease Name'}))
    reviewed = forms.ChoiceField(
        label='Reviewed Status', initial='n', choices=REVIEWED_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-inline'})
    )

    class Meta:
        model = Disease
        fields = '__all__'
        exclude = ['id', 'variant']
        ordering = ['name']


EvidenceFormset = modelformset_factory(
    Evidence, fields=['id', 'item', 'source_type', 'source_id', 'statement'],
    exclude=['disease'], min_num=0, extra=87, max_num=87
)


# SO Forms------------------------------------------------------------------------------------------------------
class BaseSODiseaseFormset(BaseCustomModelFormSet):
    def add_fields(self, form, index):
        super(BaseSODiseaseFormset, self).add_fields(form, index)
        self.set_nested(form, {FunctionalFormset: ['%s-func', Evidence], ActEvidenceFormset: ['%s-act', Evidence], ReportFormset: ['%s-report', Report]}, index)

    def set_query(self, class_name, index):
        queryset = class_name.objects.none()
        item = super(BaseSODiseaseFormset, self).set_query(class_name, index)
        if item:
            if class_name == Evidence:
                queryset = queryset | item.evidences.all()
            elif class_name == Report:
                queryset = queryset | item.reports.all()
        return queryset


class FuncEvidenceForm(forms.ModelForm):
    item = forms.ChoiceField(required=False, choices=FUNC_CAT_CHOICES)

    class Meta:
        model = Evidence
        fields = '__all__'


class SODiseaseForm(DiseaseForm):
    name = forms.ChoiceField(required=False, choices=SO_DX_CHOICES, widget=forms.Select(attrs={'placeholder': 'Disease Name'}))


SODiseaseFormset = modelformset_factory(
    Disease, form=SODiseaseForm, formset=BaseSODiseaseFormset,
    fields='__all__', exclude=['id', 'variant'], min_num=0, extra=3
)
FunctionalFormset = modelformset_factory(
    Evidence, form=FuncEvidenceForm,
    exclude=['disease'], min_num=0, extra=9
)
ActEvidenceFormset = modelformset_factory(
    Evidence, exclude=['variant', 'disease'], min_num=0, extra=3
)

ReportFormset = modelformset_factory(Report, fields='__all__', exclude=['disease'], min_num=0, extra=6, max_num=6)


# GP Forms------------------------------------------------------------------------------------------------------
class BaseGPDiseaseFormset(BaseCustomModelFormSet):
    def add_fields(self, form, index):
        super(BaseGPDiseaseFormset, self).add_fields(form, index)
        self.set_nested(form, {ScoreForm: ['%s-score', Score], EvidenceFormset: ['%s-path_item', Evidence]}, index)

    def set_query(self, class_name, index):
        queryset = class_name.objects.none()
        item = super(BaseGPDiseaseFormset, self).set_query(class_name, index)
        if item:
            if class_name == Evidence:
                queryset = queryset | item.evidences.all()
            elif class_name == Score:
                queryset = model_to_dict(item.score) if hasattr(item, 'score') else Score.objects.none().first()
        return queryset


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = '__all__'
        exclude = ['disease', 'DELETE']


GPDiseaseFormset = modelformset_factory(
    Disease, form=DiseaseForm, formset=BaseGPDiseaseFormset,
    fields='__all__', exclude=['id', 'variant'], min_num=0, extra=3
)
