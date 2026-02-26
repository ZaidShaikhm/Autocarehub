from django import forms

from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'brand', 'model', 'year']
        widgets = {
            'vehicle_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. MH01AB1234'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Maruti Suzuki'
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Swift Dzire'
            }),
            'year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2020'
            }),
        }