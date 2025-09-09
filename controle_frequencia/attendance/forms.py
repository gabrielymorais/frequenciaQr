from django import forms
import re

def _only_digits(s: str) -> str:
    return re.sub(r"\D+", "", s or "")

class ScanForm(forms.Form):
    cpf = forms.CharField(label="CPF", max_length=14)
    name = forms.CharField(label="Nome", max_length=120, required=False)

    def clean_cpf(self):
        cpf = _only_digits(self.cleaned_data["cpf"])
        if len(cpf) != 11:
            raise forms.ValidationError("CPF deve conter 11 dígitos.")
        return cpf 
