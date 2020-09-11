from django.contrib import admin
from .models import Contact, Invoice, Item, InvoiceItem
# Register your models here.

admin.site.register(Item)

class ContactAdmin(admin.ModelAdmin):
    list_display = ("contact_type", 'name','email', 'city', 'pincode')
    search_fields = ("contact_type", 'name','email', 'city', 'pincode')
admin.site.register(Contact, ContactAdmin)

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]
    extra = 1

admin.site.register(Invoice, InvoiceAdmin)
