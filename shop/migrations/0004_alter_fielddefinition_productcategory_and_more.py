# Generated by Django 5.1.4 on 2025-01-10 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_fielddefinition_listing_listingfield_productcategory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fielddefinition',
            name='productCategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_definitions', to='shop.productcategory'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='productCategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.productcategory'),
        ),
        migrations.AlterField(
            model_name='listingfield',
            name='definition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.fielddefinition'),
        ),
        migrations.AlterField(
            model_name='listingfield',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_fields', to='shop.listing'),
        ),
    ]
