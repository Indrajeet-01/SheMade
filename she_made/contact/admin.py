from django.contrib import admin
from .models import Contact, Subscribe

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'message')
    list_display_links = ('id','name')
    search_fields = ('id','name')
    list_per_page = 25

admin.site.register(Contact, ContactAdmin)

class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_per_page = 25

admin.site.register(Subscribe, SubscribeAdmin)

# Register your models here.
