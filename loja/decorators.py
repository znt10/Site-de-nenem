from django.contrib.auth.decorators import login_required, user_passes_test


def staff_required(view_func):
    """Permite acesso apenas a usuários autenticados com is_staff=True."""
    decorated = user_passes_test(lambda u: u.is_active and u.is_staff, login_url='painel:login')
    return login_required(decorated(view_func), login_url='painel:login')
