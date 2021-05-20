from django.contrib.auth.hashers import make_password


def add_users(apps, _schema_editor):
    """
    apps: ? Used; to get apps
    _schema_editor: ?; not used parameter
    return:

    Initialize User models.
    """
    User = apps.get_model('accounts', 'User')
    pwd_hash = make_password('scMN4244', hasher='pbkdf2_sha256')
    User.objects.get_or_create(username='admin', email='irene.chae@uhn.ca', password=pwd_hash, staff=True,
                               admin=True, is_superuser=True, specialist=True, counselor=True, scientist=True)

    users = ['scientist', 'counselor', 'specialist', 'staff']
    for user_str in users:
        pwd_hash = make_password(user_str, hasher='pbkdf2_sha256')
        user = User.objects.create(username=user_str, email=user_str + '@uhn.ca', password=pwd_hash, staff=True)
        if user_str in users[:3]:
            user.specialist = True
        if user_str in users[:2]:
            user.counselor = True
        if user_str == 'scientist':
            user.scientist = True
        user.save()