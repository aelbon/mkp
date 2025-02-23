from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.db.models import Prefetch
from django.views import View
from ..forms import ProductForm
from ..models import Listing, ListingImage
from ..util.util import validate_images
from ..util.log_util import log_session_info   
from django.db import connection

def index(request):
    # if request.user.is_authenticated:
    #         log_session_info('LISTING INDEX.aboutToSetUser')
    #         with connection.cursor() as cursor:
    #             cursor.execute(
    #                 "SELECT set_config('shop.current_user_id', %s, FALSE)",
    #                 [str(request.user.id)]
    #             )
    #         log_session_info('LISTING INDEX.userIsSet')
    log_session_info('LISTING INDEX GET.Start')
    products = Listing.objects.filter(store=request.current_shop).prefetch_related(
        Prefetch(
            'images',
            queryset=ListingImage.objects.only('id'),
        )
    ).all()
    return render(request, 'listing.html', {'products': products})

def listing_details(request, id):
    log_session_info('LISTING DETAILS GET.Start')
    product = Listing.objects.filter(store=request.current_shop).prefetch_related(
        Prefetch(
            'images',
            queryset=ListingImage.objects.only('id'),
        )
    ).get(id=id)
    return render(request, 'listing-details.html', {'product':product, 'display_edit': product.creator == request.user})   
class ListingCreateView(View):
        def get(self, request: HttpRequest):
            log_session_info('LISTING FORM CREATE GET.Start')
            form = ProductForm()
            return render(request, 'listing-create.html', {'form': form, 'image_errors': False})    
        def post(self, request: HttpRequest):
            log_session_info('LISTING FORM CREATE POST.Start')
            form = ProductForm(request.POST)
            valid_images, image_errors = validate_images(request)
            form.instance.creator = request.user
            if form.is_valid() and valid_images:
                log_session_info('LISTING FORM CREATE POST.aboutToSave')
                listing = form.save(commit=False)
                listing.creator = request.user  # Set the creator to the current user
                listing.store = request.current_shop # Set the store to the current store
                listing.save()
                for file in request.FILES.getlist('images'):
                    ListingImage.objects.create(
                        fileName=file.name,
                        data=file.file.read(),
                        mimetype=file.content_type,
                        listing=listing
                    )
                log_session_info('LISTING FORM POST.saved')
                return redirect('listing') 
            return render(request, 'listing-create.html', {'form': form, 'image_errors': image_errors})
        
class ListingUpdateView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        id = kwargs.get('id')
        log_session_info('LISTING FORM UPDATE GET.Start'  + str( kwargs)) 
        old_listing = None
        if id != None:
            old_listing = Listing.objects.filter(store = request.current_shop).prefetch_related(
                Prefetch(
                    'images',
                    queryset=ListingImage.objects.only('id'),
                )).get(id=id)
        form = ProductForm(instance=old_listing)
        return render(request, 'listing-create.html', {'form': form, 'image_errors': False})
    def post(self, request: HttpRequest, *args, **kwargs):
        log_session_info('LISTING FORM UPDATE POST.Start')
        id = kwargs.get('id')
        if id != None:
            old_listing = Listing.objects.filter(store = request.current_shop).prefetch_related(
                Prefetch(
                    'images',
                    queryset=ListingImage.objects.only('id'),
                )).get(id=id)
        form = ProductForm(request.POST)
        if request.FILES.getlist('images'):
            valid_images, image_errors = validate_images(request)
        else:
            valid_images = True
            image_errors = False
        form.instance.creator = request.user
        if form.is_valid() and valid_images:
            log_session_info('LISTING FORM UPDATE POST.aboutToSave')
            listing = form.save(commit=False)
            listing.id = id
            listing.timeOfCreation = old_listing.timeOfCreation
            listing.creator = old_listing.creator 
            listing.store = request.current_shop # Set the creator to the creator of the old listing
            listing.save()
            for file in request.FILES.getlist('images'):
                ListingImage.objects.create(
                    fileName=file.name,
                    data=file.file.read(),
                    mimetype=file.content_type,
                    listing=listing
                )
            log_session_info('LISTING FORM UPDATE POST.saved')
            return redirect('listing') 
        return render(request, 'listing-create.html', {'form': form, 'image_errors': image_errors})