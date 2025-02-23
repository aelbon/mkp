from django import forms
from .models import ShopCustomization

class ShopCustomizationForm(forms.ModelForm):
    class Meta:
        model = ShopCustomization
        fields = [
            'primary_color',
            'secondary_color',
            'accent_color',
            'heading_font',
            'body_font',
        ]
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color'}),
            'accent_color': forms.TextInput(attrs={'type': 'color'}),
            'heading_font': forms.Select(choices=[
                ('Arial, sans-serif', 'Arial'),
                ('Helvetica, sans-serif', 'Helvetica'),
                ('Georgia, serif', 'Georgia'),
                ('Times New Roman, serif', 'Times New Roman'),
            ]),
            'body_font': forms.Select(choices=[
                ('Arial, sans-serif', 'Arial'),
                ('Helvetica, sans-serif', 'Helvetica'),
                ('Georgia, serif', 'Georgia'),
                ('Times New Roman, serif', 'Times New Roman'),
            ]),
        }