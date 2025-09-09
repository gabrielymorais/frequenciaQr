import io
import csv
import qrcode
import re
from base64 import b64encode
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .forms import ScanForm
from .models import Attendance, AttendanceSession, Employee

# Helpers ------------------------------------------------------------
def _format_cpf(cpf_digits: str) -> str:
    """Formata 'only digits' -> 000.000.000-00 (se tiver 11 dígitos)."""
    if len(cpf_digits) == 11 and cpf_digits.isdigit():
        return f"{cpf_digits[0:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:11]}"
    return cpf_digits

def _last5(cpf_digits: str) -> str:
    return cpf_digits[-5:] if cpf_digits else ""

def _qr_image_bytes(data: str) -> bytes:
    """Gera um QR robusto e retorna bytes PNG."""
    qr = qrcode.QRCode(
        version=None,  # auto
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=3,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# util: cria (ou pega) a sessão do dia --------------------------------
def _get_or_create_today_session():
    today = timezone.localdate()
    session, _ = AttendanceSession.objects.get_or_create(
        date=today, defaults={"active": True}
    )
    return session

# Páginas -------------------------------------------------------------

# Tela do QR (com base64 de fallback para o <img onerror>)
def kiosk_qr(request):
    session = _get_or_create_today_session()
    url = request.build_absolute_uri(reverse("scan_session", args=[session.token]))

    png_bytes = _qr_image_bytes(url)
    qr_base64 = b64encode(png_bytes).decode("utf-8")

    return render(
        request,
        "attendance/kiosk.html",
        {"session": session, "qr_base64": qr_base64, "url": url},
    )

# Endpoint que serve o PNG direto (preferido pelo template)
def kiosk_qr_png(request):
    session = _get_or_create_today_session()
    url = request.build_absolute_uri(reverse("scan_session", args=[session.token]))
    return HttpResponse(_qr_image_bytes(url), content_type="image/png")

# (Opcional) Debug: mostra a URL codificada no QR
def kiosk_qr_debug(request):
    session = _get_or_create_today_session()
    url = request.build_absolute_uri(reverse("scan_session", args=[session.token]))
    return HttpResponse(url, content_type="text/plain")

# Página que o funcionário acessa ao ler o QR
def scan_session(request, token):
    session = get_object_or_404(AttendanceSession, token=token, active=True)
    today = session.date

    if request.method == "POST":
        form = ScanForm(request.POST)
        if form.is_valid():
            # aqui o cpf já vem só com dígitos do clean_cpf()
            cpf = form.cleaned_data["cpf"]
            name = form.cleaned_data.get("name", "").strip()

            with transaction.atomic():
                # cria/pega o funcionário pelo CPF normalizado
                emp, created = Employee.objects.get_or_create(
                    cpf=cpf,
                    defaults={
                        "name": name or "Sem Nome",
                        "employee_id": _last5(cpf),  # ID = 5 últimos dígitos do CPF
                    },
                )
                if not created:
                    changed = False
                    if name:
                        emp.name = name
                        changed = True
                    # garante consistência do ID (5 últimos) se estava diferente
                    new_id = _last5(emp.cpf)
                    if emp.employee_id != new_id:
                        emp.employee_id = new_id
                        changed = True
                    if changed:
                        emp.save()

                att, _ = Attendance.objects.get_or_create(
                    employee=emp, date=today, defaults={"session": session}
                )

                now = timezone.now()
                if att.check_in is None:
                    att.check_in = now
                    action = "entrada"
                elif att.check_out is None:
                    att.check_out = now
                    action = "saida"
                else:
                    action = "finalizado"

                att.session = session
                att.save()

            return render(
                request,
                "attendance/scan.html",
                {
                    "session": session,
                    "form": ScanForm(),
                    "success": True,
                    "action": action,
                    "att": att,
                },
            )
    else:
        form = ScanForm()

    return render(request, "attendance/scan.html", {"session": session, "form": form})

def dashboard(request):
    date = timezone.localdate()
    q = (
        Attendance.objects.filter(date=date)
        .select_related("employee")
        .order_by("employee__name")
    )
    query = request.GET.get("q", "").strip()
    if query:
        q = q.filter(employee__name__icontains=query)

    total_segundos = sum(int(a.hours_worked.total_seconds()) for a in q)
    total_horas = total_segundos // 3600
    total_min = (total_segundos % 3600) // 60

    return render(
        request,
        "attendance/dashboard.html",
        {
            "date": date,
            "records": q,
            "query": query,
            "total_label": f"{total_horas}h {total_min}min",
            "format_cpf": _format_cpf,
        },
    )

def export_csv(request):
    date = timezone.localdate()
    q = (
        Attendance.objects.filter(date=date)
        .select_related("employee")
        .order_by("employee__name")
    )

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename=frequencia_{date}.csv"

    writer = csv.writer(response)
    writer.writerow(["Nome", "ID (últ.5)", "CPF", "Data", "Entrada", "Saída", "Horas Trabalhadas (min)"])
    for a in q:
        cpf_digits = a.employee.cpf or ""
        mins = int(a.hours_worked.total_seconds() // 60) if a.hours_worked else 0
        writer.writerow(
            [
                a.employee.name,
                _last5(cpf_digits),                 # ID = últimos 5
                _format_cpf(cpf_digits),            # CPF com máscara
                a.date.isoformat(),
                a.check_in.astimezone().strftime("%H:%M") if a.check_in else "",
                a.check_out.astimezone().strftime("%H:%M") if a.check_out else "",
                mins,
            ]
        )
    return response
