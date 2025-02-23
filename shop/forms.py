from django import forms
from .models import Listing, ProductCategory, FieldDefinition, ListingImage, Shop, Image
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.sites.models import Site


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name']
class FieldDefinitionForm(forms.ModelForm):
    class Meta:
        model = FieldDefinition
        fields = ['name', 'subcategory', 'fieldType']

FieldDefinitionFormSet = inlineformset_factory(
    ProductCategory, FieldDefinition, form=FieldDefinitionForm, extra=10, can_delete=True
)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title','status','referenceNumber', 'manufacturer', 'model', 'description', 'price', 'location', 'availability', 'condition']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['fileName', 'data']
        
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'logo', 'owner']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['fileName', 'data', 'mimetype']

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['domain', 'name']



SiteFormSet = forms.modelformset_factory(Site, form=SiteForm, extra=1, can_delete=True)