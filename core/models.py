from django.db import models

# Create your models here.
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICE = (
    ("processing", "Processing"),
    ("delivered", "Delivered"),
    ("shipped", "Shipped"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "★✰✰✰✰"),
    (2, "★★✰✰✰"),
    (3, "★★★✰✰"),
    (4,"★★★★✰"),
    (5,"★★★★★"),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20,
                         prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, unique=True, default="Food")
    image = models.ImageField(upload_to="category", default="category.jpg")
    date = models.DateTimeField(auto_now_add=True, null=True,blank=True)

    class Meta:
        verbose_name_plural = "Category"

    class MPTTMeta:
        order_insertion_by = ['title']

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20,
                         prefix="ven", alphabet="abcdefgh12345")
    
    title = models.CharField(max_length=100, default="Adepa")
    cover_image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")

    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    # description = models.TextField(null=True, blank=True, default="I sell good products only")
    description = RichTextUploadingField(null=True, blank=True, default="I sell good products only")


    address = models.CharField(
        max_length=200, default="123 Main street, Suame")
    contact = models.CharField(max_length=200, default="+233")
    shipping_on_time = models.CharField(max_length=200, default="100")
    chat_resp_time = models.CharField(max_length=200, default="100")
    authentic_rating = models.CharField(max_length=200, default="100")
    day_return = models.CharField(max_length=200, default="100")
    waranty_period = models.CharField(max_length=200, default="100")
    date = models.DateTimeField(auto_now_add=True, null=True,blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet = "abcdefgh12345")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="product")


    title = models.CharField(max_length=100, default="Fresh pear")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    # description = models.TextField(null=True, blank=True, default="This is the product")
    description = RichTextUploadingField(null=True, blank=True, default="I sell good products only")

    price = models.DecimalField(max_digits=99999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=99999999, decimal_places=2, default="2.99")
    # specifications = models.TextField(null=True, blank=True, default="Black")
    specifications = RichTextUploadingField(null=True, blank=True, default="Black")

    type = models.CharField(max_length=100, default="Organic", null=True, blank=True)
    stock_count = models.CharField(max_length=100, default="8", null=True, blank=True)
    life = models.CharField(max_length=100, default="100", null=True, blank=True )
    size = models.CharField(max_length=100, default="L", null=True, blank=True )
    color = models.CharField(max_length=100, default="Blue", null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)
 
    tags = TaggableManager(blank=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix ="SKU", alphabet = "1234567890")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)



    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price - self.old_price) / (self.price) * 100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product_images", default="product.jpg")
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Images"


###################################cart, order, orderitems and address #######################
###################################cart, order, orderitems and address #######################
###################################cart, order, orderitems and address #######################
###################################cart, order, orderitems and address #######################





class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=99999999, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")


    class Meta:
        verbose_name_plural = "Cart Order"



class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField( max_length=200,)
    item = models.CharField( max_length=200,)
    image = models.CharField( max_length=200,)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999999, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=99999999, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"


    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))



################################### product review, whishlist, address #######################
################################### product review, whishlist, address #######################
################################### product review, whishlist, address #######################
################################### product review, whishlist, address #######################
################################### product review, whishlist, address #######################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=300, null=True)
    email = models.CharField(max_length=300, null=True)
    mobile = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"



