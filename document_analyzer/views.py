from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction

from .models import Document, DocumentSection
from .forms import DocumentUploadForm
from .services import LLMService

@login_required
def index(request):
    """Main page for document analyzer"""
    form = DocumentUploadForm()
    documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    
    return render(request, 'document_analyzer/index.html', {
        'form': form,
        'documents': documents
    })

@login_required
@require_POST
def upload_document(request):
    """Handle document upload and processing"""
    form = DocumentUploadForm(request.POST, request.FILES)
    
    if form.is_valid():
        # Create document but don't save to DB yet
        document = form.save(commit=False)
        document.user = request.user
        
        with transaction.atomic():
            # Save document to get an ID
            document.save()
            
            try:
                # Process with LLM
                sections = LLMService.analyze_document(document)
                
                # Save all sections
                DocumentSection.objects.bulk_create(sections)
                
                # Return the table partial with HTMX
                return render(request, 'document_analyzer/table_partial.html', {
                    'document': document,
                    'sections': sections
                })
            except Exception as e:
                # If there's an error, delete the document and return error
                document.delete()
                return HttpResponse(f"Error processing document: {str(e)}", status=500)
    
    # Form is invalid
    return HttpResponse("Invalid form submission", status=400)

@login_required
def get_document(request, document_id):
    """Get a single document and its sections"""
    document = get_object_or_404(Document, id=document_id, user=request.user)
    sections = document.sections.all()
    
    return render(request, 'document_analyzer/index.html', {
        'form': DocumentUploadForm(),
        'document': document,
        'sections': sections,
        'documents': Document.objects.filter(user=request.user).order_by('-uploaded_at')
    })

@login_required
@require_POST
def update_section(request, section_id):
    """Update a single section via HTMX"""
    section = get_object_or_404(DocumentSection, id=section_id)
    
    # Ensure user owns the document
    if section.document.user != request.user:
        return HttpResponse("Unauthorized", status=403)
    
    # Update fields
    field = request.POST.get('field')
    value = request.POST.get('value')
    
    if field and value and hasattr(section, field):
        try:
            # Convert to float for numeric fields
            if field in ['x_position', 'y_position', 'width', 'height']:
                value = float(value)
            
            # Update the field
            setattr(section, field, value)
            section.save()
            
            # Return success
            return HttpResponse(value)
        except ValueError:
            return HttpResponse("Invalid value", status=400)
    
    return HttpResponse("Invalid request", status=400)

@login_required
def get_preview(request, document_id):
    """Get the layout preview partial"""
    document = get_object_or_404(Document, id=document_id, user=request.user)
    sections = document.sections.all()
    
    # Debug info
    print(f"Preview requested for document {document_id}")
    print(f"Found {sections.count()} sections")
    for section in sections:
        print(f"Section: {section.section_name}, Position: ({section.x_position}, {section.y_position}), Size: {section.width}x{section.height}")
    
    return render(request, 'document_analyzer/preview_partial.html', {
        'document': document,
        'sections': sections
    })

@login_required
def debug_sections(request, document_id):
    """Debug view to check section data"""
    document = get_object_or_404(Document, id=document_id, user=request.user)
    sections = document.sections.all()
    
    sections_data = []
    for section in sections:
        sections_data.append({
            'id': section.id,
            'name': section.section_name,
            'x': section.x_position,
            'y': section.y_position,
            'width': section.width,
            'height': section.height,
        })
    
    return JsonResponse({
        'document_id': document_id,
        'sections_count': len(sections_data),
        'sections': sections_data
    })
