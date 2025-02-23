from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_group_permissions(sender, **kwargs):
    group, _ = Group.objects.get_or_create(name="Visitor")
    # Example of adding permissions
    permissions = Permission.objects.filter(
        codename__in=[
            "view_listing",
            "view_productcategory",
            "view_fielddefinition",
            "view_listingimage",
            "view_listingfield",
            "add_listing",
            "add_listingimage",
            "add_listingfield",
            "change_listing",
            "change_listingimage",
            "change_listingfield",
            "delete_listing",
            "delete_listingimage",
            "delete_listingfield",
            "view_productcategory",
        ]
    )
    group.permissions.add(*permissions)
    
      