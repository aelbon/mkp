# Generated by Django 5.1.4 on 2025-01-11 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_fielddefinition_productcategory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='availability',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='condition',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='creator',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='location',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='manufacturer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='model',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='referenceNumber',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='store',
            field=models.CharField(max_length=255),
        ),
    ]
