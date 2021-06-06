from itertools import chain

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from accounts.models import User
from .constants import *

__all__ = [
    'Gene', 'Variant', 'Disease', 'History', 'PredPMID', 'CancerHotspot',
    'Score', 'Evidence', 'Report', 'ITEMS', 'VariantField'
]


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = []

    def __str__(self):
        """ The string method """
        return self.class_type()

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
    gene_curation_notes = models.TextField(verbose_name='Gene Curation Notes', max_length=255, blank=True, default='')

    class Meta:
        ordering = ['name']

    def __str__(self):
        """ The string method """
        return self.name


class Variant(BaseModel):
    """ A class used to represent a Variant object """
    gene = models.ForeignKey(Gene, related_name='variants', on_delete=models.CASCADE)
    cdna = models.CharField(verbose_name='c.', max_length=10, default='')
    protein = models.CharField(verbose_name='p.', max_length=20, unique=True)

    chr = models.CharField(verbose_name='Chromosome', max_length=6, default='')
    transcript = models.CharField(max_length=20)
    start = models.CharField(max_length=10, default='')
    end = models.CharField(max_length=10, default='')
    ref = models.CharField(max_length=100, default='')
    alt = models.CharField(max_length=100, default='')
    content = models.TextField(verbose_name='Curation Notes', blank=True)
    germline_content = models.TextField(blank=True)

    class Meta:
        ordering = ['protein']

    def __str__(self):
        """ The string method """
        return self.protein

    def get_pane(self, item):
        pane_item, rtn_dict = {
            'main': ['transcript', 'chr', 'start', 'end', 'ref', 'alt'],
            'detail': [
                'exonicfunc.uhnclggene', 'af', 'af_popmax', 'cosmic70', 'clinvar',
                'insilicodamaging', 'insilicobenign', 'tcga#occurances'
            ],
            'score': ['oncokb', 'oncokb_pmids', 'watson', 'watson_pmids', 'qci', 'qci_pmids', 'jaxckb'],
            'link': ['google', 'civic', 'alamut'],
        }.get(item, []), {}
        verbose_dict = {field.name: field.verbose_name for field in self._meta.fields}
        for field_name in pane_item:
            var_field = VariantField.get_value(self.id, field_name)
            rtn_dict[verbose_dict.get(field_name, field_name)] = self.serializable_value(field_name) if item == 'main' else var_field if field_name != 'pmid_list' else ''
        return rtn_dict.items()


class VariantField(BaseModel):
    name = models.CharField(verbose_name='field name', max_length=50, default='')
    value = models.CharField(max_length=500, default='')
    variant = models.ForeignKey(Variant, related_name='fields', on_delete=models.CASCADE, null=True, blank=True)

    @staticmethod
    def get_value(var_id, field_name):
        try:
            value = VariantField.objects.get(variant=var_id, name=field_name).value
        except VariantField.DoesNotExist:
            value = 'N/A'
        return value


class CancerHotspot(BaseModel):
    """ A class used to represent a Cancer hotspot object """
    hotspot = models.CharField(max_length=70, default='')
    count = models.IntegerField(default=1)
    variant = models.ForeignKey(Variant, related_name='hotspots', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """ The string method """
        return self.hotspot


# Delete
class PredPMID(BaseModel):
    name = models.CharField(max_length=40, default='')
    value = models.CharField(max_length=40, default='')
    pmids = models.CharField(max_length=50, default='')
    variant = models.ForeignKey(Variant, related_name='pmid_list', on_delete=models.CASCADE, null=True, blank=True)


class Disease(BaseModel):
    """ A class used to represent a Disease object """
    name = models.CharField(max_length=50)
    branch = models.CharField(choices=BRANCH_CHOICES, max_length=2, default='no')
    func_sig = models.CharField(verbose_name='Functional Significance', choices=FUNC_SIG_CHOICES, max_length=20, null=True, blank=True)
    others = models.CharField(verbose_name='Tier', choices=TIER_CHOICES, max_length=20, null=True, blank=True)
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
        print(ITEMS.keys())
        if self.item:
            return list(ITEMS.keys())[int(self.item)] if self.item.isnumeric() else self.item
        return 'Actionability'


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
