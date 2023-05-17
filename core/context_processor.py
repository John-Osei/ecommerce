from django.shortcuts import get_object_or_404
from core.models import Product,ProductImages,Category,Vendor,CartOrder,CartOrderItem,Wishlist,Address,ProductReview
from django.db.models import Min, Max
from django.contrib import messages
from userauths.models import Profile
from taggit.models import Tag



def default(request, tag_slug=None):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    recently_added = Product.objects.all().order_by("-date")[:3]
    deals = Product.objects.all().order_by("-date")[2:6]
    product = Product.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))


    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.filter(user=request.user)
        except:
            messages.warning(request, "You need to login before accessing your wishlist.")
            wishlist = 0
    else:
        wishlist = 0

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None

    return {
        'categories':categories,
        'wishlist':wishlist,
        'address':address,
        'vendors':vendors,
        'min_max_price':min_max_price,
        "recently_added":recently_added,
        "deals":deals,
        "product":product,
        # "user_profile": user_profile,
    }