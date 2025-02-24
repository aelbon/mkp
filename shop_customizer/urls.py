from django.urls import path
from . import views

app_name = 'shop_customizer'

urlpatterns = [
    # Main customization view - can be accessed at both / and /customize/
    path('', views.ShopCustomizerView.as_view(), name='customize'),
    path('customize/', views.ShopCustomizerView.as_view(), name='customize'),
    
    # Preview page with both form and preview
    path('preview/', views.PreviewView.as_view(), name='preview_page'),
    
    # HTMX endpoint for live preview updates
    path('preview-update/', views.preview, name='preview'),
    
    # Endpoint for saving final customization
    path('save-customization/', views.SaveCustomizationView.as_view(), name='save_customization'),
]