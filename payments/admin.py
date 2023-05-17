from django.contrib import admin
from . models import Payment, UserWallet

# Register your models here.


class PaymentAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['id','user', 'amount', 'ref', 'email', 'verified', 'date_created']

admin.site.register(Payment, PaymentAdmin)
admin.site.register(UserWallet)
