def add_null_diseases(apps, _schema_editor):
    Disease = apps.get_model('api', 'Disease')
    for i in range(10):
        if i < 5:
            Disease.objects.create(name='', branch='so', report='', reviewed='n', variant_id=None, others='', curation_notes='')
        else:
            Disease.objects.create(name='', branch='gp', report='', reviewed='n', variant_id=None, others='', curation_notes='')

# migrations.RunPython(add_null_diseases)
