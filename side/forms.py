from django import forms

__all__ = ['ListTextWidget', 'SearchForm']

from api.constants import GP_DX_CHOICES, SO_DX_CHOICES


class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list': '%s_list' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="%s_list">' % self._name
        for item in self._list:
            data_list += '<option value="%s">%s</option>' % (item[0], item[1])
        data_list += '</datalist>'

        return text_html + data_list


class SearchForm(forms.Form):
    gene__name__icontains = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Gene Name'}))
    cdna__icontains = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'C.'}))
    protein__icontains = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'P.'}))
    diseases__name__icontains = forms.ChoiceField(
        required=False, choices=SO_DX_CHOICES, widget=forms.Select(attrs={'placeholder': 'Disease Name'})
    )
    diseases__name__icontains2 = forms.ChoiceField(
        required=False, choices=GP_DX_CHOICES, widget=forms.Select(attrs={'placeholder': 'Disease Name'})
    )
