from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ShopCustomization
from .forms import ShopCustomizationForm
from django.http import JsonResponse
from django.views import View

class ShopCustomizerView(LoginRequiredMixin, UpdateView):

    model = ShopCustomization
    form_class = ShopCustomizationForm
    template_name = 'shop_customizer/customize.html'
    success_url = reverse_lazy('shop_customizer:preview')
    
    def get_object(self):
        # Changed from 'shop' to 'owner'
        obj, created = ShopCustomization.objects.get_or_create(
            owner=self.request.user
        )
        return obj

class PreviewView(LoginRequiredMixin, TemplateView):

    template_name = 'shop_customizer/preview.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Changed from 'shop' to 'owner'
        customization, created = ShopCustomization.objects.get_or_create(
            owner=self.request.user
        )
        context['customization'] = customization
        return context

class SaveCustomizationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        customization = ShopCustomization.objects.get(owner=request.user)
        form = ShopCustomizationForm(request.POST, instance=customization)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})