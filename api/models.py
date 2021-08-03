from itertools import chain

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from accounts.models import User
from .constants import *

__all__ = ['Gene', 'GeneField', 'Variant', 'Disease', 'Review', 'History', 'CancerHotspot', 'Score', 'Evidence', 'Report', 'ITEMS', 'VariantField']


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

    region = models.CharField('Actionable Regions', max_length=50, null=True, blank=True)
    gene_curation_notes = models.TextField(verbose_name='Gene Curation Notes', max_length=255, blank=True, default='')
    reviewed_date = models.DateTimeField('Last Reviewed Date', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """ The string method """
        return self.name

    def get_values(self):
        return []


class GeneField(BaseModel):
    name = models.CharField('field name', max_length=50, default='', choices=[
        ('actionable', 'Actionable In'),
        ('not_actionable', 'Not Actionable In'),
        ('mut_type', 'Actionable Mutation Types'),
    ])
    group = models.CharField(max_length=50, null=True, blank=True)
    value = models.CharField(max_length=50, default='')
    gene = models.ForeignKey(Gene, related_name='actionability', on_delete=models.CASCADE)


class Variant(BaseModel):
    """ A class used to represent a Variant object """
    gene = models.ForeignKey(Gene, related_name='variants', on_delete=models.CASCADE)
    cdna = models.CharField('c.', max_length=60, default='')  # TODO: max length longer
    protein = models.CharField('p.', max_length=60)

    chr = models.CharField('Chromosome', max_length=6, default='')
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
                                      'ExonicFunc.UHNCLGGene', 'AF', 'AF_Popmax', 'Cosmic70', 'Clinvar',
                                      'InSilicoDamaging', 'InSilicoBenign', 'TCGA#occurances'
                                  ],
                                  'score': ['OncoKB', 'OncoKB_PMIDs', 'Watson', 'Watson_PMIDs', 'QCI', 'QCI_PMIDs', 'JAX_variant'],
                                  'link': ['Google', 'CIViC', 'Alamut'],
                              }.get(item, []), {}
        verbose_dict = {field.name: field.verbose_name for field in self._meta.fields}
        for field_name in pane_item:
            var_field = VariantField.get_value(self.id, field_name.lower())
            rtn_dict[verbose_dict.get(field_name, field_name)] = self.serializable_value(field_name) if item == 'main' else var_field
        return rtn_dict.items()


class VariantField(BaseModel):
    name = models.CharField('field name', max_length=50, default='')
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


class Disease(BaseModel):
    """ A class used to represent a Disease object """
    name = models.CharField(max_length=50)
    branch = models.CharField(choices=BRANCH_CHOICES, max_length=2, default='no')
    func_sig = models.CharField('Functional Significance', choices=FUNC_SIG_CHOICES, max_length=20, null=True, blank=True)
    others = models.CharField('Tier', choices=TIER_CHOICES, max_length=20, null=True, blank=True)
    # report = models.TextField('Germline Report', max_length=255, blank=True, default='')
    variant = models.ForeignKey(Variant, related_name='diseases', on_delete=models.CASCADE, null=True, blank=True)

    reviewed = models.CharField(choices=REVIEWED_CHOICES, max_length=1, default='n')
    curation_notes = models.TextField('Curation Notes', max_length=255, blank=True, default='')

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
        review = Review.objects.filter(disease=self)
        return review.last().date if review.count() else None


class Review(BaseModel):
    review = models.CharField(choices=REVIEWED_CHOICES, max_length=1)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField('date', auto_now_add=True)
    disease = models.ForeignKey(Disease, related_name='reviews', on_delete=models.CASCADE)


class Score(BaseModel):
    """ A class used to represent a Score object """
    for_score = models.CharField('For Pathogenicity', max_length=20, default='Uncertain')
    against_score = models.CharField('Against Pathogenicity', max_length=20, default='Uncertain')
    content = models.CharField('ACMG Classification', max_length=100, default='Uncertain')
    disease = models.OneToOneField(Disease, related_name='score', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """ The string method """
        return self.for_score + ' ' + self.against_score + '\n' + self.content


class Evidence(BaseModel):
    """ A class used to represent a Evidence object """
    item = models.CharField('Functional Category', max_length=75, default='', blank=True)
    source_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    source_id = models.CharField(max_length=20, blank=True, default='')
    statement = models.TextField(null=True, blank=True, default='')

    evid_sig = models.CharField(
        'Evidence Significance', max_length=4,
        choices=EVID_SIG_CHOICES, null=True, blank=True
    )
    level = models.CharField(
        'Evidence Level', max_length=1,
        choices=EVID_LEVEL_CHOICES, null=True, blank=True
    )
    evid_dir = models.BooleanField(
        'Evidence Direction', choices=EVID_DIR_CHOICES,
        null=True, blank=True
    )
    clin_sig = models.CharField(
        'Clinical Significance', choices=CLIN_SIG_CHOICES,
        max_length=25, null=True, blank=True
    )
    drug_class = models.TextField('Drug/Drug Class/Dx', null=True, blank=True)
    evid_rating = models.IntegerField(
        'Evidence Rating', choices=EVID_RATING_CHOICES,
        null=True, blank=True
    )
    disease = models.ForeignKey(Disease, related_name='evidences', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """ The string method """
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
