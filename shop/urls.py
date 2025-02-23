from django.urls import path

from .views import auth, image, listing, view, shop

urlpatterns = [
    path("", view.index, name="index"),
    path("listing", listing.index, name="listing"),
    path("listing/create", listing.ListingCreateView.as_view(), name="listing-create"),
    path("listing/create/<int:id>", listing.ListingUpdateView.as_view(), name="listing-create-id"),
    path("listing/details/<int:id>", listing.listing_details, name='listing-details'),
    path("faq", view.faq, name="faq"),
    path("register", auth.register, name="register"),
    path("login", auth.user_login, name="login"),
    path("logout", auth.user_logout, name="logout"),
    path('productcategory/create', view.create_product_category, name='productcategory-create'),
    path('images/<int:image_id>', image.images, name='images'),
    path('create-shop/', shop.create_shop, name='create_shop')
]