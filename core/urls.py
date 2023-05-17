from django.urls import include, path
from core import views

from admin_notification.views import check_notification_view



app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.product_list_view, name="product-list"),

    path("newsletter/", views.newsletter, name ="newsletter"),


    
    ################ PRODUCT ###############
    path("product/<pid>/", views.product_detail_view, name="product-detail"),
    # path("about/", about_view, name="about"),



    ########################   CATEGORY   ########################
    path("category/", views.category_list_view, name="category-list"),
    path("category/<cid>/", views.category_product_list_view, name="category-product-list"),


    ############################  VENDOR  ####################
    path("vendors/", views.vendor_list_view, name="vendor-list"),
    path("vendors/<vid>/", views.vendor_detail_view, name="vendor-detail"),


    ############## tags###########################
    path("products/tag/<slug:tag_slug>/", views.tag_list, name="tags"),

    ### Add review
    path("ajax-add-review/<int:pid>/", views.ajax_add_review, name="ajax-add-review"),

    #search
    path("search/", views.search_view, name="search"),

    #filter 
    path("filter-products/", views.filter_product, name="filter-product"),

    ####Add to cart
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),

    ## Cart page 
    path("cart/", views.cart_view, name="cart"),

    path("delete-from-cart/", views.delete_item_from_cart, name="delete-from-cart"),

        #### Update cart
    path("update-cart/", views.update_cart, name="update-cart"),


    # Checkout  URL
    path("checkout/", views.checkout_view, name="checkout"),

    #Paypal URL
    path('paypal/', include('paypal.standard.ipn.urls')),

     # Payment Successful
    path("payment-completed/", views.payment_completed_view, name="payment-completed"),

    # Payment Failed
    path("payment-failed/", views.payment_failed_view, name="payment-failed"),

     # Dahboard URL
    path("dashboard/", views.customer_dashboard, name="dashboard"),

    # Order Detail URL
    path("dashboard/order/<int:id>", views.order_detail, name="order-detail"),

    # Making address defauly
    path("make-default-address/", views.make_address_default, name="make-default-address"),

    # wishlist page
    path("wishlist/", views.wishlist_view, name="wishlist"),

    # adding to wishlist
    path("add-to-wishlist/", views.add_to_wishlist, name="add-to-wishlist"),


    # Remvoing from wishlist
    path("remove-from-wishlist/", views.remove_wishlist, name="remove-from-wishlist"),


    path("contact/", views.contact, name="contact"),
    path("ajax-contact-form/", views.ajax_contact_form, name="ajax-contact-form"),

        ############ABOUT###########
    path("about_us/", views.about_us, name="about_us"),
    path("best_Price/", views.best_price, name="best_price"),
    path("wide_assortment/", views.wide_assortment, name="wide_assortment"),
    path("free_delivery/", views.free_delivery, name="free_delivery"),
    path("easy_returns/", views.easy_returns, name="easy_returns"),
    path("great_deal/", views.great_deal, name="great_deal"),
    path("satisfaction/", views.satisfaction, name="satisfaction"),

       ###############

    path("purchase_guide/", views.purchase_guide, name="purchase_guide"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("terms_of_service/", views.terms_of_service, name="terms_of_service"),


    #Notification

    path('check/notification/', check_notification_view, name="check_notifications"),










]