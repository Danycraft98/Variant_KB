from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
# from weasyprint import HTML, CSS

from api.models import *
from api.tables import VariantTable
from .forms import *
from .functions import *
from .tables import *

PROTEIN_DICT = {
    'A': 'Ala', 'R': 'Arg', 'N': 'Asn', 'D': 'Asp', 'C': 'Cys', 'Q': 'Gln', 'E': 'Glu',
    'G': 'Gly', 'H': 'His', 'I': 'Ile', 'L': 'Leu', 'K': 'Lys', 'M': 'Met', 'F': 'Phe',
    'P': 'Pro', 'S': 'Ser', 'T': 'Thr', 'W': 'Trp', 'Y': 'Tyr', 'V': 'Val', 'B': 'Asx',
    'Z': 'Glx', 'J': 'Xle', 'U': 'Sec', 'O': 'Pyl', 'X': 'Unk', 'fs': 'Ter'
}


@login_required
def search(request):
    search_form = SearchForm(request.POST or None, request.FILES or None)
    if search_form.is_valid():
        search_query = {key: val for key, val in search_form.cleaned_data.items() if key != 'csrfmiddlewaretoken' and val}
        disease2 = search_query.pop('diseases__name__icontains2', None)
        protein = search_query.pop('protein__icontains', None)
        if protein:
            search_query.update({'protein__icontains': PROTEIN_DICT[protein.upper()] if protein.upper() in PROTEIN_DICT else protein})
        if disease2:
            search_query.update({'diseases__name__icontains': disease2})
        print(search_query)
        variant_list = VariantTable(Variant.objects.filter(**search_query))
        return render(request, 'variants/index.html', {'table': variant_list, 'title': ('pe-7s-search', 'Search Result', '')})
    return render(request, 'general/search.html', {'form': search_form, 'title': ('pe-7s-search', 'Search', 'Find the variant information by search.')})


@login_required
def account_request(request):
    if request.POST:
        send_mail(
            'Account User Level Request',
            'Dear Sir/Madam,\nI am requesting for user level ' + request.POST.get('level', '') + '. My username is ' + request.user.username + '\nRegards,\n' + request.POST.get('name', 'anonymous'),
            request.POST.get('email', 'anonymous@variant.com'),
            ['lee.daniel.jhl@gmail.com'],
            fail_silently=False
        )
        return render(request, 'general/request.html', {'title': 'List of Genes'})
    return render(request, 'general/request.html', {'title': 'List of Genes'})


@login_required
def upload(request):
    switch, upload_file, submit_list = False, request.FILES.get('file', None), request.POST.getlist('submit', None)
    if upload_file:
        if 'xlsx' in upload_file.name:
            switch = True
            filename = os.path.join(os.getenv('BASE_DIR'), 'static', upload_file.name.replace('xlsx', 'csv').replace('xls', 'csv'))
            read_file(upload_file, dtype=str).to_csv(filename, index=False)
            upload_file = open(filename)
        line, found = True, False
        while line:
            line = upload_file.readline()
            line = line.split(',') if switch else line.decode().split(',')
            if 'Disease' in line[0]:
                found = True
            elif not line[0] and found or all(not col for col in line):
                break

        raw_data = read_file(upload_file, dtype=str)
        raw_data.fillna('na', inplace=True)
        raw_data.columns = map(str.lower, raw_data.columns)

        cols = list(raw_data.columns)
        [cols.remove(key) for key in ['gene', 'protein']]
        cols = ['gene', 'protein'] + cols
        raw_data = raw_data[cols]

        raw_data.insert(0, '^'.join(raw_data.head()), raw_data.agg('^'.join, axis=1))
        raw_data.insert(1, 'Exists', '')
        for index, row in raw_data.iterrows():
            raw_data.at[index, 'Exists'] = 'Exist' if Variant.objects.filter(gene__name=row['gene'], protein=row['protein']).count() > 0 else 'New'
        raw_data.sort_values('Exists', inplace=True)
        return render(request, 'general/upload.html', {
            'tables': (raw_data.to_html(index=False, classes='exist table table-bordered table-hover', justify='left')),
            'file': upload_file, 'title': ('pe-7s-upload', 'Uploads', 'Review the upload data.')
        })

    elif submit_list:
        pmids = ['oncokb', 'watson', 'qci', 'jaxckb']
        headers, values = request.POST.get('headers', None).split('^'), request.POST.getlist('row_val', None)
        for submit in submit_list:
            values = submit.split('^')
            gene, protein, row = values.pop(0), values[0], dict(zip(headers[1:], values))
            [row.pop(key, '') for key in ['igv', 'ucsc genome browser', 'hgmd']]
            gene_obj, gene_exists = Gene.objects.update_or_create(name=gene)
            row.update({
                'exonic_function': row.pop('exonicfunc.uhnclggene', 'na'),
                'tcga': row.pop('tcga#occurances', 'na')
            })
            raw_cancerhotspot = row.pop('cancerhotspots', 'na').split('|')
            add_vals, pred_pmids, pop_list = [key for key in row if key in pmids or 'pred' in key], [], ['id']
            for key in add_vals:
                pred_pmid = PredPMID.objects.create(name=key, value=row.pop(key), pmids=row.pop(key + '_pmids')) if key in pmids \
                    else PredPMID.objects.create(name=key, value=row.pop(key))
                pred_pmids.append(pred_pmid)

            for name in row:
                try:
                    Variant._meta.get_field(name)
                except FieldDoesNotExist:
                    pop_list.append(name)
            [row.pop(name, None) for name in pop_list]
            new_variant, _ = Variant.objects.get_or_create(gene=gene_obj, **row)
            History.objects.create(content='Update' if new_variant.history.count() else 'Upload', timestamp=timezone.now(), user=request.user, variant=new_variant)
            for pred_pmid in pred_pmids:
                pred_pmid.variant = new_variant
                pred_pmid.save()
            for hotspot in raw_cancerhotspot:
                if hotspot == 'na':
                    break
                values = hotspot.split(':')
                CancerHotspot.objects.create(hotspot=values[0], count=int(values[1]) if len(values) > 1 else 0, variant=new_variant)
    return redirect('index')


@login_required
def history(request, gene_name, protein):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=protein)
        histories = HistoryTable([h for h in item.history.all()])
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    return render(request, 'variants/index.html', {'item': item, 'table': histories, 'title': ('pe-7s-timer', 'History - {protein}'.format(protein=item.protein), 'View the history of variant, {protein}.'.format(protein=item.protein))})


@login_required
def export(request, gene_name, protein):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=protein)
        disease_list = DiseaseTable(item.diseases.all())
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    return render(request, 'variants/index.html', {'title': ('pe-7s-export', 'Export for Variant', 'Export the variant information.'), 'item': item, 'table': disease_list})


def exported(request, gene_name, protein):
    try:
        item = Variant.objects.get(gene__name=gene_name, protein=protein)
    except Variant.DoesNotExist:
        raise Http404('Variant does not exist')
    diseases = Disease.objects.filter(name__in=request.POST.getlist('disease'), variant=item)
    """html = HTML(string=render_to_string('general/export.html', {'item': item, 'diseases': diseases, 'user': request.user}))
    html.write_pdf(target='/tmp/report.pdf', stylesheets=[
        CSS('static/css/bootstrap.min.css'), CSS('static/css/main.css')
    ])"""

    fs = FileSystemStorage('/tmp')
    with fs.open('report.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = "attachment; filename=report.pdf"
        return response
