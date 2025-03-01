from django.contrib import admin
from .models import Document, DocumentSection

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at')
    search_fields = ('title', 'user__username')
    list_filter = ('uploaded_at',)

@admin.register(DocumentSection)
class DocumentSectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'document', 'x_position', 'y_position', 'width', 'height')
    search_fields = ('section_name', 'content', 'document__title')
    list_filter = ('document',)
    