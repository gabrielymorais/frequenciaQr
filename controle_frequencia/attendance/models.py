import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=120)
    employee_id = models.CharField(max_length=50, unique=True)
    cpf = models.CharField(max_length=14, unique=True)  # formato 000.000.000-00 ou numérico

    def __str__(self):
        return f"{self.name} ({self.employee_id})"

class AttendanceSession(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date = models.DateField(default=timezone.localdate, db_index=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("date",)
        ordering = ["-date"]

    def __str__(self):
        return f"Sessão {self.date} ({'ativa' if self.active else 'inativa'})"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate, db_index=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    hours_worked = models.DurationField(default=timedelta(0))
    session = models.ForeignKey(AttendanceSession, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-date", "employee__name"]
        unique_together = ("employee", "date")

    def compute_hours(self):
        if self.check_in and self.check_out:
            self.hours_worked = self.check_out - self.check_in
        else:
            self.hours_worked = timedelta(0)

    def save(self, *args, **kwargs):
        self.compute_hours()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} - {self.date}"