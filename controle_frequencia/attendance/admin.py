from django.contrib import admin
from .models import Employee, Attendance, AttendanceSession

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "employee_id", "cpf")
    search_fields = ("name", "employee_id", "cpf")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "check_in", "check_out", "hours_worked")
    list_filter = ("date",)
    search_fields = ("employee__name", "employee__employee_id", "employee__cpf")

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ("date", "token", "active")
    list_filter = ("active", "date")