from django.contrib import admin

from home.models import Setting ,ContactFormMessage,UserProfile

# Register your models here.
class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name','email', 'message','note','subject','status']
    list_filter = ['status']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','phone','address','city','country','image_tag']

admin.site.register(Setting)
admin.site.register(ContactFormMessage, ContactFormMessageAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
