from django import template

register = template.Library()

@register.filter
def cpf_mask(cpf_digits: str) -> str:
    s = "".join(ch for ch in (cpf_digits or "") if ch.isdigit())
    if len(s) == 11:
        return f"{s[0:3]}.{s[3:6]}.{s[6:9]}-{s[9:11]}"
    return cpf_digits or ""

@register.filter
def duration_hhmm(value):
    """
    Mostra 1:51 (HH:MM), arredondando os segundos.
    Se value for None/vazio, retorna '-'.
    """
    if not value:
        return "-"
    total = int(round(value.total_seconds()))
    hours, rem = divmod(total, 3600)
    minutes, _seconds = divmod(rem, 60)
    return f"{hours}:{minutes:02d}"

@register.filter
def duration_hhmmss(value):
    """
    Versão com segundos: 1:51:10 (HH:MM:SS)
    """
    if not value:
        return "-"
    total = int(round(value.total_seconds()))
    hours, rem = divmod(total, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}"
