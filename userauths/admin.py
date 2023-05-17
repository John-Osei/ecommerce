from django.contrib import admin
from userauths.models import MailMessage, User, ContactUs, Profile, SubscribedUsers

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']


class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date')

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'full_name', 'bio', 'phone']


admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile)
admin.site.register(SubscribedUsers, SubscribedUsersAdmin)
admin.site.register(MailMessage)

