from django.db import models
from django.conf import settings

class ShopLayout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    template = models.CharField(max_length=100)
    
    # Define available sections and their types
    sections = models.JSONField(default=list)
    
    def get_default_sections():
        return [
            {
                "id": "header",
                "type": "header",
                "title": "Store Header",
                "options": {
                    "show_search": True,
                    "show_cart": True
                }
            },
            {
                "id": "featured_products",
                "type": "product_list",
                "title": "Featured Products",
                "options": {
                    "products_per_row": 3,
                    "show_price": True
                }
            }
        ]

class ShopCustomization(models.Model):
    # Changed from 'shop' to 'owner' to better reflect the relationship
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='shop_customization'  # Added related_name for easier querying
    )
    
    # Basic theme settings
    primary_color = models.CharField(max_length=7, default="#000000")
    secondary_color = models.CharField(max_length=7, default="#ffffff")
    accent_color = models.CharField(max_length=7, default="#007bff")
    
    # Typography
    heading_font = models.CharField(max_length=100, default="Arial")
    body_font = models.CharField(max_length=100, default="Arial")
    
    # Section-specific settings
    section_settings = models.JSONField(default=dict)

    def __str__(self):
        return f"Shop customization for {self.owner.username}"