from itertools import chain

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from accounts.models import User
from .constants import *

__all__ = [
    'Gene', 'Variant', 'Disease', 'History', 'PredPMID',
    'CancerHotspot', 'Score', 'Evidence', 'Report', 'ITEMS'
]


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = []

    def __str__(self):
        """ The string method """
        return ''

    def count(self):
        """ The object count method """
        return self.__class__.objects.all().count()

    def class_type(self):
        """ The class type method """
        return self.__class__.__name__

    def get_fields(self, fields=None, exclude=None):
        opts, data = self._meta, {}
        for field in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            if not getattr(field, 'editable', False):
                continue
            if fields is not None and field.name not in fields:
                continue
            if exclude and field.name in exclude:
                continue
            data[field.verbose_name] = self._get_FIELD_display(field)
        return data


class Gene(BaseModel):
    """ A class used to represent a Gene object """
    name = models.CharField(max_length=20)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    content = models.TextField(null=True, blank=True)
    germline_content = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """ The string method """
        return self.name


class Variant(BaseModel):  # TODO: possibly remove genome_build, consequence
    """ A class used to represent a Variant object """
    genome_build = models.CharField(max_length=10, default='')
    chr = models.CharField(verbose_name='Chromosome', max_length=6, default='')
    start = models.CharField(max_length=10, default='')
    end = models.CharField(max_length=10, default='')
    ref = models.CharField(max_length=100, default='')
    alt = models.CharField(max_length=100, default='')
    transcript = models.CharField(max_length=20)
    cdna = models.CharField(verbose_name='c.', max_length=10, default='')
    protein = models.CharField(verbose_name='p.', max_length=20)
    consequence = models.CharField(max_length=10, default='')
    exonic_function = models.CharField(max_length=20, default='')
    content = models.TextField(verbose_name='Curation Notes', blank=True)
    germline_content = models.TextField(blank=True)

    af = models.CharField(verbose_name='AF', max_length=20, default='')
    af_popmax = models.CharField(verbose_name='AF_popmax', max_length=20, default='')
    cosmic70 = models.CharField(max_length=500, default='')
    clinvar = models.CharField(verbose_name='CLINVAR', max_length=20, default='')
    insilicodamaging = models.CharField(verbose_name='InSilicoDamaging', max_length=100, default='')
    insilicobenign = models.CharField(verbose_name='InSilicoBenign', max_length=100, default='')
    tcga = models.CharField(verbose_name='TCGA#occurances', max_length=20, default='')
    pmkb = models.CharField(verbose_name='Live PMKB Classification', max_length=10, default='')
    pmkb_citations = models.CharField(verbose_name='PMKB citations', max_length=500, default='')
    civic = models.CharField(verbose_name='CIViC', max_length=50, default='')
    google = models.CharField(max_length=100, default='')
    alamut = models.CharField(max_length=70, default='')
    gene = models.ForeignKey(Gene, related_name='variants', on_delete=models.CASCADE)

    class Meta:
        ordering = ['protein']

    def __str__(self):
        """ The string method """
        return self.protein

    def get_pane(self, item):
        pane_item = {
            'main': ['transcript', 'chr', 'start', 'end', 'ref', 'alt'],
            'detail': [
                'exonic_function', 'af', 'af_popmax', 'cosmic70', 'clinvar', 'insilicodamaging',
                'insilicobenign', 'pmid_list', 'tcga'
            ],
            'score': ['pmid_list'],
            'link': ['google', 'civic', 'alamut'],
        }.get(item, [])
        verbose_dict = {field.name: field.verbose_name for field in self._meta.fields}
        return {verbose_dict.get(field, 'pred_pmid'): self.serializable_value(field) if field != 'pmid_list' else field for field in pane_item}.items()


class PredPMID(BaseModel):
    name = models.CharField(max_length=40, default='')
    value = models.CharField(max_length=40, default='')
    pmids = models.CharField(max_length=50, default='')
    variant = models.ForeignKey(Variant, related_name='pmid_list', on_delete=models.CASCADE, null=True, blank=True)


class CancerHotspot(BaseModel):
    """ A class used to represent a Cancer hotspot object """
    hotspot = models.CharField(max_length=70, default='')
    count = models.IntegerField(default=1)
    variant = models.ForeignKey(Variant, related_name='hotspots', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """ The string method """
        return self.hotspot


class Disease(BaseModel):
    """ A class used to represent a Disease object """
    name = models.CharField(max_length=50)
    branch = models.CharField(choices=BRANCH_CHOICES, max_length=2, default='no')
    func_sig = models.CharField(verbose_name='Functional Significance', choices=FUNC_SIG_CHOICES, max_length=20, null=True, blank=True)
    others = models.CharField(choices=TIER_CHOICES, max_length=20, null=True, blank=True)
    report = models.TextField(verbose_name='Germline Report', max_length=255, blank=True, default='')
    variant = models.ForeignKey(Variant, related_name='diseases', on_delete=models.CASCADE, null=True, blank=True)

    reviewed = models.CharField(choices=REVIEWED_CHOICES, max_length=1, default='n')
    reviewed_date = models.DateTimeField('reviewed date', null=True, blank=True)
    review_user = models.ForeignKey(User, related_name='reviewed_variants', on_delete=models.CASCADE, null=True, blank=True)
    meta_reviewed_date = models.DateTimeField('meta-reviewed date', null=True, blank=True)
    meta_review_user = models.ForeignKey(User, related_name='meta_reviewed_variants', on_delete=models.CASCADE, null=True, blank=True)
    approved_date = models.DateTimeField('approved date', null=True, blank=True)
    approve_user = models.ForeignKey(User, related_name='approved_variants', on_delete=models.CASCADE, null=True, blank=True)
    curation_notes = models.TextField(verbose_name='Curation Notes', max_length=255, blank=True, default='')

    def __str__(self):
        """ The string method """
        return self.name

    def count(self):
        """ The Disease count method """
        return self.__class__.objects.filter(~Q(name='')).count()

    @staticmethod
    def none():
        diseases = {
            'so': Disease.objects.filter(variant=None, branch='so'),
            'gp': Disease.objects.filter(variant=None, branch='gp')
        }
        for branch, disease_list in diseases.items():
            if 5 - disease_list.count() <= 0:
                continue
            for _ in range(5 - disease_list.count()):
                Disease.objects.create(branch=branch, report='', reviewed='n', variant=None, others='')
        return Disease.objects.filter(variant=None)

    def clean(self):
        super(Disease, self).clean()
        if not self.name or self.name == '':
            raise ValidationError('Please enter proper name.')
        elif not self.branch or self.branch == 'no':
            raise ValidationError('NO branch cannot be a branch.')
        if hasattr(self, 'score') and self.score:
            self.score.delete()

    def get_date(self):
        return self.approved_date if self.approved_date else self.meta_reviewed_date if self.meta_reviewed_date\
            else self.reviewed_date if self.reviewed_date else None


class Score(BaseModel):
    """ A class used to represent a Score object """
    for_score = models.CharField(verbose_name='For Pathogenicity', max_length=20, default='Uncertain')
    against_score = models.CharField(verbose_name='Against Pathogenicity', max_length=20, default='Uncertain')
    content = models.CharField(verbose_name='ACMG Classification', max_length=100, default='Uncertain')
    disease = models.OneToOneField(Disease, related_name='score', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """ The string method """
        return self.for_score + ' ' + self.against_score + '\n' + self.content


class Evidence(BaseModel):
    """ A class used to represent a Evidence object """
    item = models.CharField(verbose_name='Functional Category', max_length=75, default='', blank=True)
    source_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    source_id = models.CharField(max_length=20, blank=True, default='')
    statement = models.TextField(null=True, blank=True, default='')

    evid_sig = models.CharField(
        verbose_name='Evidence Significance', max_length=4,
        choices=EVID_SIG_CHOICES, null=True, blank=True
    )
    level = models.CharField(
        verbose_name='Evidence Level', max_length=1,
        choices=EVID_LEVEL_CHOICES, null=True, blank=True
    )
    evid_dir = models.BooleanField(
        verbose_name='Evidence Direction', choices=EVID_DIR_CHOICES,
        null=True, blank=True
    )
    clin_sig = models.CharField(
        verbose_name='Clinical Significance', choices=CLIN_SIG_CHOICES,
        max_length=25, null=True, blank=True
    )
    drug_class = models.TextField(verbose_name='Drug/Drug Class/Dx', null=True, blank=True)
    evid_rating = models.IntegerField(
        verbose_name='Evidence Rating', choices=EVID_RATING_CHOICES,
        null=True, blank=True
    )
    disease = models.ForeignKey(Disease, related_name='evidences', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """ The string method """
        return str(self.item) if self.item else self.statement


class Report(BaseModel):
    report_name = models.CharField(max_length=40)
    content = models.TextField(null=True, blank=True)
    gene = models.ForeignKey(Gene, related_name='reports', on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='reports', on_delete=models.CASCADE, null=True, blank=True)
    disease = models.ForeignKey(Disease, related_name='reports', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """ The string method """
        return self.content

    def clean(self):
        super(Report, self).clean()
        if not self.content:
            raise ValidationError('Wrong Key')


class History(BaseModel):
    """ A class used to represent a History object """
    content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    object = models.ForeignKey(Evidence, verbose_name='field', related_name='histories', on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='history', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """ Order by timestamp """
        ordering = ['timestamp']

    def __str__(self):
        """ The string method """
        return str(self.user) + ' / ' + self.timestamp.strftime('%Y-%m-%d')
