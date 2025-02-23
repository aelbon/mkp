import json
import os
import mimetypes
import logging
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from shop.models import Shop, Image

IMAGE_DIRECTORY = 'shop/images'

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_initial_data():
    with open('shop/initialData.json', 'r') as file:
        data = json.load(file)

        # Load users
        for user_data in data['users']:
            username = user_data['username']
            email = user_data['email']
            password = user_data['password']

            user, created = User.objects.get_or_create(username=username, defaults={'email': email})
            if created:
                user.set_password(password)
                user.save()
            else:
                user.email = email
                user.set_password(password)  # Important: Update password even if user exists
                user.save()

        # Load shops and sites
        for shop_data in data['shops']:
            shop_name = shop_data['name']
            description = shop_data['description']
            owner_data = shop_data['owner']
            owner_username = owner_data['username']

            try:
                owner = User.objects.get(username=owner_username)
            except User.DoesNotExist:
                logger.warning(f"Owner with username {owner_username} does not exist.")
                continue

            shop, created = Shop.objects.get_or_create(name=shop_name, defaults={'description': description, 'owner': owner})
            if not created:
                shop.owner = owner
                shop.description = description
                shop.save()  # Save after updating owner and description

            # Handle logo
            if 'logo' in shop_data:
                file_name = shop_data['logo']
                image_path = os.path.join(IMAGE_DIRECTORY, file_name)

                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()

                mimetype, _ = mimetypes.guess_type(image_path)

                image, created = Image.objects.get_or_create(fileName=file_name, defaults={'data': image_data, 'mimetype': mimetype})
                if not created:
                    image.data = image_data
                    image.mimetype = mimetype
                    image.save()

                shop.logo = image
                shop.save()  # Save after setting logo

            # Load sites and associate with shop AFTER saving the shop
            for site_data in shop_data['sites']:
                domain = site_data['domain']
                name = site_data['name']
                site, created = Site.objects.get_or_create(domain=domain, defaults={'name': name})
                if not created:
                    site.name = name
                site.save()  # Ensure the site is saved before adding to the relationship
                # logger.debug(f"Site saved: {site.id} - {site.domain}")
                shop.sites.add(site)
            shop.save()

class Command(BaseCommand):
    help = 'Load initial sites, users, and shops from a JSON file'

    def handle(self, *args, **kwargs):
        load_initial_data()