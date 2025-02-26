from django.urls import path
from . import views

app_name = 'document_analyzer'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_document, name='upload_document'),
    path('document/<int:document_id>/', views.get_document, name='get_document'),
    path('section/<int:section_id>/update/', views.update_section, name='update_section'),
    path('document/<int:document_id>/preview/', views.get_preview, name='get_preview'),
    path('document/<int:document_id>/debug/', views.debug_sections, name='debug_sections'),
]

