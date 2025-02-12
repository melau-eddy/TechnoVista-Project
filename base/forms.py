from django import forms
from .models import Reserve, Contact

class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reserve
        fields = ['name', 'email', 'arrival_date', 'due_date', 'population']  
        widgets = {
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'subject', 'message', 'phone', 'date']
        widgets = {
            'date' : forms.DateInput(attrs={'type' : 'date'})
        }