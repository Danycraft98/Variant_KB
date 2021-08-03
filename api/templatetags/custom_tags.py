import re

from django import template

from api.constants import *

register = template.Library()


@register.filter
def get_prefix(form):
    end = form.prefix.rindex('-')
    start = form.prefix.rindex('-', 0, end)
    if not re.search('\\d+$', form.prefix):
        start, end = end, len(form.prefix)
    return form.prefix[start + 1:end]


@register.filter
def exec_method(obj, item=None):
    try:
        return obj.get_pane(item) if hasattr(obj, 'get_pane') else obj.get_values()
    except AttributeError:
        print('AttributeError')


@register.filter('filter')
def detailed_filter(obj, filter_txt):
    try:
        raw_list = obj.filter(name=filter_txt)
        return [[field.group, field.value] for field in raw_list] if filter_txt != 'mut_type' else [field.value for field in raw_list]
    except AttributeError:
        print('AttributeError')


@register.filter
def get_header(form):
    return_types = {
        'func': 'Functional Evidences', 'score': 'ACMG 2015 Score',
        'act': 'Actionability Evidences', 'report': 'Reports'
    }
    return return_types.get(get_prefix(form), None)


@register.filter
def get_review_val(val):
    for item in REVIEWED_CHOICES:
        if item[0] == val:
            return item[1]
    return 'Not reviewed'


@register.filter
def get_label(field, index):
    if not field:
        try:
            index = list(ITEMS)[min(int(index), 28)]
        except ValueError:
            index = list(ITEMS)[0]
        return '{key}: {val}'.format(key=index, val=ITEMS[index][0])
    elif not hasattr(field, 'auto_id'):
        return field
    match = re.search('(report|path_item)-\\d+-([^-]+)$', field.auto_id)
    index = index if not match or match.group(1) == 'report' else list(ITEMS)[min(index, 28)]
    if match and (match.group(1) == 'report' or match.group(2) == 'item'):
        return REPORT_NAMES[min(index, 5)] + ':' if match.group(1) == 'report' else '{key}: {val}'.format(key=index, val=ITEMS[index][0])
    return 'Functional Class:' if 'Item:' in field.label_tag() else field.label_tag()


@register.filter
def get_fields(form, index=None):
    return_fields = []
    if get_prefix(form) == 'path_item' and index:
        index = index if index else 0
        return ITEMS[list(ITEMS)[min(index, 28)]][1]
    for field in form.visible_fields():
        if field.name in RETURN_TYPE.get(get_prefix(form), []):
            return_fields.append(field)
    return return_fields[index] if index is not None else return_fields


@register.filter
def get_values(item, is_path=False):
    prefix = CLASS_TO_PREFIX.get(item.class_type(), None) if hasattr(item, 'class_type') else None
    prefix = 'evid' if hasattr(item, 'item') and item.item and not item.disease.branch == 'so' else prefix
    obj_dict = item.get_fields(fields=RETURN_TYPE.get(prefix, [])) if hasattr(item, 'get_fields') else []
    return ITEMS[list(ITEMS)[min(item, 28)]][1] if is_path else obj_dict.items()


@register.filter
def get_div_or_link(value, arg):
    if type(value) == str:
        return ";".join(["<a href='http://pubmed.ncbi.nlm.nih.gov/" + pmid + "' target='_blank'>" + pmid + '</a>' for pmid in value.split(arg)])
    return 'border-bottom pb-2 mb-2' if value and not arg else ''


@register.filter
def is_empty(form, is_first=False):
    if type(form) == str:
        return form == 'detail' and not is_first or form == 'score' and is_first
    elif get_prefix(form) in ['path_item', 'report', 'dx'] and is_first != 'path':
        return False
    fields = [field for field in get_fields(form) if field.name in ['source_id', 'statement']] if is_first == 'path' else get_fields(form)
    is_first = False if is_first == 'path' else is_first
    return all(not field.value() for field in fields) and not is_first


@register.filter
def is_special_case(field, index):
    match = re.search('(func|report)-\\d+-(key|report(?:_name)?)$', field.auto_id)
    match_dict = {'dx': ['report', True], 'func': ['key', index], 'report': ['report_name', True]}
    found = match_dict.get(match.group(1), None) if match else None
    return not (found and match.group(2) == found[0] and found[1]) if found else not match


@register.filter
def math(num1, num2):
    if type(num1) != int:
        return num1 == num2
    return [num1 // num2, num1 % num2] if num2 != 0 else [0, 0]
