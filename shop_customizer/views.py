from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import ShopCustomization
from .forms import ShopCustomizationForm

class ShopCustomizerView(LoginRequiredMixin, UpdateView):
    model = ShopCustomization
    form_class = ShopCustomizationForm
    template_name = 'shop_customizer/customize.html'
    success_url = reverse_lazy('shop_customizer:preview')
    
    def get_object(self):
        # Get or create customization for the current user
        obj, created = ShopCustomization.objects.get_or_create(
            owner=self.request.user
        )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customization'] = self.get_object()
        return context

class PreviewView(LoginRequiredMixin, TemplateView):
    template_name = 'shop_customizer/preview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the customization object and create form instance
        customization = ShopCustomization.objects.get_or_create(
            owner=self.request.user
        )[0]
        context['customization'] = customization
        context['form'] = ShopCustomizationForm(instance=customization)
        return context

def preview(request):
    """Handle HTMX updates for the preview"""
    if not request.user.is_authenticated:
        return HttpResponse("Authentication required", status=403)
        
    try:
        # Get current customization
        customization = ShopCustomization.objects.get(owner=request.user)
        
        if request.method == 'POST':
            # Update customization with POST data without saving to database
            form = ShopCustomizationForm(request.POST, instance=customization)
            if form.is_valid():
                # Don't save to database yet - just update the instance
                customization = form.save(commit=False)
            
        # Render the preview with either updated or current customization
        return render(
            request, 
            'shop_customizer/preview_content.html',
            {
                'customization': customization,
                'form': ShopCustomizationForm(instance=customization)
            }
        )
                     
    except ShopCustomization.DoesNotExist:
        return HttpResponse("Shop customization not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error updating preview: {str(e)}", status=500)

class SaveCustomizationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            customization = ShopCustomization.objects.get(owner=request.user)
            form = ShopCustomizationForm(request.POST, instance=customization)
            
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Customization saved successfully'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Form validation failed',
                    'errors': form.errors
                }, status=400)
                
        except ShopCustomization.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Customization not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)