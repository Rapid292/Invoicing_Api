from django.contrib import admin
from .models import Contact, Invoice, Item, InvoiceItem, Payment
# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ("contact_type", 'name','email', 'city', 'pincode')
    search_fields = ("contact_type", 'name','email', 'city', 'pincode')
admin.site.register(Contact, ContactAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ("item_code", 'title','gst_rate', 'description')
    search_fields = ("item_code", 'title','gst_rate' )
admin.site.register(Item, ItemAdmin)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem

class Payment(admin.TabularInline):
    model = Payment
    

class InvoiceAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,               {'fields': ['invoi']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]
    inlines = [InvoiceItemInline, Payment]
    extra = 1

admin.site.register(Invoice, InvoiceAdmin)
