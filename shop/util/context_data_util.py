from django.contrib.sites.models import Site
from shop.models import Shop
from django.contrib.sites.shortcuts import get_current_site
def get_current_site_and_shop(request):
    """
    Retrieve the current site and shop based on the host name.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        A tuple containing the current site and shop.
    """
    try:
        current_site = get_current_site(request)
        current_shop = Shop.objects.only('id', 'name', 'description', 'owner_id', 'logo_id').get(sites=current_site)
        return current_site, current_shop
    except Site.DoesNotExist:
        return None, None
    except Shop.DoesNotExist:
        return current_site, None