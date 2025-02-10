from django import forms
from .models import Reserve

class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reserve
        fields = ['name', 'email', 'arrival_date', 'due_date', 'population']  
        widgets = {
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }
