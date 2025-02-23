from django.shortcuts import render, redirect
from ..forms import ProductCategoryForm, FieldDefinitionFormSet


def index(request):
    return render(request, 'index.html')


def faq(request):
    return render(request, 'faq.html')


# def register(request):
    # return render(request, 'register.html')

    
def create_product_category(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        formset = FieldDefinitionFormSet(request.POST, instance=form.instance)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('productcategory-create.html')  # Replace with your success URL
    else:
        form = ProductCategoryForm()
        formset = FieldDefinitionFormSet(instance=form.instance)
    return render(request, 'productcategory-create.html', {'form': form, 'formset': formset})




