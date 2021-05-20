from api.models import History


def save_formset(formset, other_fields=None):
    final_save, other_fields = False, other_fields if other_fields else {}
    new_items = []
    if hasattr(formset, 'forms'):
        for form in formset.forms:
            new_item, is_saved = save_form(form, other_fields)
            new_items.append(new_item)
            final_save = is_saved if is_saved else final_save
    else:
        return save_form(formset, other_fields)
    return new_items, final_save


def save_form(form, other_fields=None):
    other_fields, new_item = other_fields if other_fields else {}, None
    is_evid = any(item in form.prefix for item in ['act', 'func', 'report'])
    if form.is_valid() and (
            (is_evid and (form.cleaned_data.get('source_type', '') or form.cleaned_data.get('content', '')))
            or not is_evid
    ):
        new_item = form.save()
        for attr, value in other_fields.items():
            setattr(new_item, attr, value)
        new_item.save()
        sub_fields = {new_item.class_type().lower(): new_item}
        if new_item.class_type() == 'Item':
            sub_fields.update(other_fields)
        elif new_item.class_type() == 'Evidence':
            History.objects.create(content=new_item.statement, object=new_item, variant=new_item.disease.variant)

        if hasattr(form, 'nested'):  # and not formset._should_delete_form(form):
            if type(form.nested) == list:
                [save_formset(sub_form, sub_fields) for sub_form in form.nested]
            elif form.nested.is_valid():
                save_formset(form.nested, sub_fields)
    else:
        print(form.prefix, form.errors)
    return new_item, new_item is not None
