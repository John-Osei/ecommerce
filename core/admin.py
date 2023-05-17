from django.contrib import admin

from core.models import Product,ProductImages,Category,Vendor,CartOrder,CartOrderItem, Wishlist,Wishlist,Address,ProductReview

# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    list_editable = ['featured','product_status']
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', "price",'category', 'vendor', 'featured', 'product_status', 'pid']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'image',]


    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status','product_status']
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty','price', 'total']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', "date"]

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date', 'review', 'rating']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']



admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItem, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)


