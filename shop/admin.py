from django.contrib import admin
from .models import Listing, ProductCategory, FieldDefinition

# Register your models here.
admin.site.register(Listing)
admin.site.register(ProductCategory)
admin.site.register(FieldDefinition)