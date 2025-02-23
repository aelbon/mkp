from django.db import migrations

def load_initial_data(apps, schema_editor):
    from shop.management.commands.load_initial_data import load_initial_data as load_data
    load_data()

class Migration(migrations.Migration):
    dependencies = [
       ('shop', '0012_image_remove_listingimage_data_and_more'),
    ]

    operations = [
        migrations.RunPython   (load_initial_data),
        # migrations.RunSQL(
        #     """
        #   delete from django_site where domain like '%soops.intern';
        #   delete from auth_user where username like 'admin_%';
        #     """
        # )
    ]