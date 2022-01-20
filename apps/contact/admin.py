from django.contrib import admin

# Register your models here.
from apps.contact.models import Contact, Interest


class ContactAdmin(admin.ModelAdmin):
    list_display = ['uid', 'email', 'first_name', 'last_name', 'email', 'phone', 'company']


class InterestAdmin(admin.ModelAdmin):
    list_display = ['contact', 'url', 'category', 'value',]


admin.site.register(Contact, ContactAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.site_header = 'Lost metrics'
admin.site.site_title = 'Lost metrics'