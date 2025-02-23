from django.urls import path
from . import views

app_name = 'shop_customizer'

urlpatterns = [
    path('', views.ShopCustomizerView.as_view(), name='customize'),
    path('customize/', views.ShopCustomizerView.as_view(), name='customize'),
    path('preview/', views.PreviewView.as_view(), name='preview'),
    path('save-customization/', views.SaveCustomizationView.as_view(), name='save_customization'),
]