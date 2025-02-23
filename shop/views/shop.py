from django.shortcuts import render, redirect
from shop.forms import ShopForm, SiteFormSet


def create_shop(request):
    if request.method == 'POST':
        shop_form = ShopForm(request.POST, request.FILES)
        site_formset = SiteFormSet(request.POST, request.FILES)
        if shop_form.is_valid() and site_formset.is_valid():
            shop = shop_form.save()
            site_formset.instance = shop
            site_formset.save()
            return redirect('shop_list')  # Redirect to a list of shops or another appropriate view
    else:
        shop_form = ShopForm()
        site_formset = SiteFormSet()

    return render(request, 'create_shop.html', {
        'shop_form': shop_form,
        'site_formset': site_formset,
    })