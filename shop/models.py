from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
# Image model
class Image(models.Model):
    fileName = models.CharField(max_length=255)
    data = models.BinaryField(editable=True)
    mimetype = models.CharField(max_length=255) 
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.fileName   
# Shop model
class Shop(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    logo = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='shops', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    sites = models.ManyToManyField(Site, related_name='shops')
    def __str__(self):
        return self.name


# Product Category model

class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name
class FieldType(models.TextChoices):
    TEXT = 'text', 'Text'
    NUMBER = 'number', 'Number'
    BOOLEAN = 'boolean', 'Boolean'
class ListingStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    DRAFT = 'draft', 'Draft'
    FINALIZED = 'finalized', 'Finalized'
    RESERVED = 'reserved', 'Reserved'
class FieldDefinition(models.Model):
    name = models.CharField(max_length=255)
    productCategory = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='field_definitions', blank=True, null=True)
    subcategory = models.CharField(max_length=128)
    fieldType = models.CharField(
        max_length=9,
        choices=FieldType.choices,
        default=FieldType.TEXT
    )
    def __str__(self):
        return  self.name
#  Listing model



class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, null=False)
    store  =models.ForeignKey(Shop, on_delete=models.CASCADE,  related_name='listings', blank=True, null=True)
    status  = models.CharField(
        max_length=9,
        choices=ListingStatus.choices,
        default=ListingStatus.DRAFT
    )
    referenceNumber  = models.CharField(max_length=255)
    manufacturer   = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    availability  = models.CharField(max_length=255)
    condition   = models.CharField(max_length=255)
    productCategory = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=True, null=True)
    timeOfCreation = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class ListingField(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_fields', blank=True, null=True)
    definition = models.ForeignKey(FieldDefinition, on_delete=models.CASCADE, blank=True, null=True)
    booleanContents = models.BooleanField()
    textContents = models.TextField()
    numberContents = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.definition

# ListingImage model subclassing Image with multi-table inheritance
class ListingImage(Image):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')