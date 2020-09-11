from django.db import models

# Create your models here.
class Contact(models.Model):
    CONTACT_CHOICES = (
        ('V', 'VENDOR'),
        ('C', 'CUSTOMER')
    )
    contact_type = models.CharField(max_length=1, choices=CONTACT_CHOICES)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    address_line_1 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    pincode = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} and Type={self.contact_type}"

class Invoice(models.Model):
    user = models.ForeignKey(Contact, on_delete=models.CASCADE)
    invoice_no = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    tax_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    sub_total = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user.name} and Amount={self.total}"

class Item(models.Model):
    item_code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    sale_price = models.DecimalField(default=0, max_digits=10, decimal_places=2,help_text='(INR)')
    purchase_price = models.DecimalField(default=0, max_digits=10, decimal_places=2,help_text='(INR)')
    description = models.TextField()
    gst_rate = models.FloatField(help_text='(%)')
    tds_rate = models.FloatField(help_text='(%)', null=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if self.gst_rate:
            self.gst_rate /= 100
        
        if self.tds_rate:
            self.tds_rate /= 100
        super(Item, self).save(*args, **kwargs)


class InvoiceItem(models.Model):
    user = models.ForeignKey(Contact, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    sub_total = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    tax_total = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user.name} - {self.invoice.invoice_no}"

    # def save(self, *args, **kwargs):
    #     invoiced_item = Item.objects.filter(item_code = self.pk)









