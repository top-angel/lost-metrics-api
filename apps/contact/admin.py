from django.contrib import admin

# Register your models here.
from apps.contact.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ['uid', 'email', 'first_name', 'last_name', 'email', 'phone', 'company']


admin.site.register(Contact, ContactAdmin)