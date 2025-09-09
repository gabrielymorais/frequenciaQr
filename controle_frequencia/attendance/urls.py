from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("export/csv/", views.export_csv, name="export_csv"),

    path("session/new/", views.kiosk_qr, name="kiosk_qr"),
    path("session/qr.png", views.kiosk_qr_png, name="kiosk_qr_png"),  # ← rota da imagem
    path("session/qr-url", views.kiosk_qr_debug, name="kiosk_qr_debug"),  # opcional p/ depurar
    path("s/<uuid:token>/", views.scan_session, name="scan_session"),
]
