# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='analyzer_documents/')  # Changed from 'documents/'
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analyzer_documents')  # Added related_name

    def __str__(self):
        return self.title

class DocumentSection(models.Model):
    document = models.ForeignKey(Document, related_name='sections', on_delete=models.CASCADE)
    section_name = models.CharField(max_length=100)
    content = models.TextField()
    x_position = models.FloatField()
    y_position = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return f"{self.document.title} - {self.section_name}"