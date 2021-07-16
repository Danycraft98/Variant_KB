from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from api.forms import *
from api.functions import *
from api.tables import *
from side.forms import SearchForm


def index(request):
    search_form = SearchForm(request.POST or None, request.FILES or None)
    models = [Gene, Variant, Disease]
    mini_tables = [
        GeneCardTable(Gene.objects.order_by('-pub_date')[:15]),
        VariantCardTable(Variant.objects.order_by('-gene__pub_date')[:15]),
        DiseaseCardTable(Disease.objects.filter(~Q(name='')).order_by('-reports__gene__pub_date')[:15])
    ]
    history_table = HistoryTable(History.objects.order_by('-timestamp')[:5])
    return render(request, 'general/index.html', {
        'models': models, 'mini_tables': mini_tables, 'history_table': history_table, 'form': search_form,
        'title': ('pe-7s-rocket', 'Variant-KB Dashboard', 'Bootstrap is the most popular HTML, CSS, and JS framework for developing responsive, mobile-first projects on the web.')
    })


@login_required
def genes(request):
    gene_list = GeneTable(Gene.objects.all())
    return render(request, 'variants/index.html', {'table': gene_list, 'title': ('pe-7s-display2', 'List of Genes', '')})


@login_required
def gene(request, gene_name=None):
    if not gene_name:
        title = ('pe-7s-display2', 'List of Variants', '')
        variant_list = VariantTable(Variant.objects.all())
    else:
        gene_item = Gene.objects.get(name=gene_name)
        title = ('pe-7s-display2', 'Gene: {name}'.format(name=gene_name), 'Reports here')  # gene_item.reports.al())
        variant_list = VariantTable(gene_item.variants.all())
    return render(request, 'variants/index.html', {'table': variant_list, 'title': title})


@login_required
def variant(request, gene_name, protein):
    item = get_object_or_404(Variant, gene__name=gene_name, protein=protein)
    param = {
        'item': item, 'panes': {'main': 'Variant Description', 'detail': 'Outside Databases', 'score': 'Outside Cancer Knowledge-bases', 'link': 'Links'}.items(),
        'title': (
            'pe-7s-note', 'Detail - {item}'.format(item=item),
            'Gene: {gene}; Disease Count: {count}'.format(gene=item.gene, count=item.diseases.count())
        )
    }

    if 'detail' in request.path or not request.user.is_staff:
        if not request.user.is_staff:
            messages.warning(request, 'You are not authorized to edit variants.')
        return render(request, 'variants/detail.html', param)

    param.update({
        'gene_form': GeneForm(request.POST or None, request.FILES or None, initial=item.gene.__dict__),
        'forms': [
            SODiseaseFormset(request.POST or None, request.FILES or None, prefix='so-dx', queryset=item.diseases.filter(branch='so')),
            GPDiseaseFormset(request.POST or None, request.FILES or None, prefix='gp-dx', queryset=item.diseases.filter(branch='gp'))
        ], 'item_list': ITEMS.items(), 'title': (
            'pe-7s-note', 'Edit - {item}'.format(item=item),
            'Gene: {gene}; Disease Count: {count}'.format(gene=item.gene, count=item.diseases.count())
        ), 'user': request.user
    })
    if request.method == 'POST':
        if param.get('gene_form').is_valid():
            Gene.objects.filter(id=item.gene.id).update(**param.get('gene_form').cleaned_data, reviewed_date=timezone.now())
        else:
            print(param.get('gene_form').errors)

        final_save = param.get('gene_form').is_valid()
        for formset in param.get('forms'):
            new_dxs, is_saved = save_formset(formset, {'variant': item}, True)
            for form in formset.forms:
                gene_curation_notes = form.cleaned_data.get('gene_curation_notes', None)
                if gene_curation_notes:
                    item.gene.gene_curation_notes = gene_curation_notes
                    item.gene.save()
                    break
            final_save = True if is_saved else final_save
            for dx in new_dxs:
                if not dx or dx.reviewed == 'n':
                    continue

                review, exist = Review.objects.get_or_create(review=dx.reviewed, disease_id=dx.id)
                if exist:
                    review.user = param.get('user')
                    History.objects.update_or_create(content='Reviewed status changed to {status}.'.format(status=dx.get_reviewed_display(), variant=item, user=param.get('user')))
                    review.save()

        if final_save:
            return HttpResponseRedirect(reverse('variant_text', args=[gene_name, protein]))
    return render(request, 'variants/form.html', param)
