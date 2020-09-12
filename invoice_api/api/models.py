from django.db import models
from django.utils import timezone
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
    country = models.CharField(max_length=255, blank=True, default="India")

    def __str__(self):
        return f"{self.name}"


class Invoice(models.Model):
    invoice_no = models.IntegerField(unique=True, blank=True, null=True)
    user = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='invoices')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    tax_total = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    sub_total = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    pending_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    payment_status = models.CharField(max_length=255, blank=True, default="UnderPaid")
    due_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"Invoice_Number {self.invoice_no}"

    def save(self, *args, **kwargs):
        # if self.pk == None:
        #     self.Invoice_no = 1
        # else:
        #     last_invoice = Invoice.objects.all().order_by('-id')[0]
        #     self.invoice_no = last_invoice.pk + 1
        invoice_items = InvoiceItem.objects.filter(invoice = self.pk)
        payments = Payment.objects.filter(invoice = self.pk)

        if invoice_items:
            new_sub_total = 0
            new_tax_total = 0
            for invoice_item in invoice_items:
                new_sub_total += invoice_item.amount
                new_tax_total += invoice_item.tax_amount
            self.tax_total = new_tax_total
            self.sub_total = new_sub_total
            self.total = self.tax_total + self.sub_total

        if payments:
            total_payments = 0
            for payment in payments:
                total_payments += payment.payment
            self.pending_amount = self.total - total_payments
        else:
            self.pending_amount = self.total
        
        if self.pending_amount == 0:
            self.payment_status = "Paid"
        elif self.pending_amount >= 0:
            self.payment_status = "Underpaid"
        else:
            self.payment_status = 'Overpaid'

        super(Invoice, self).save(*args, **kwargs)

    

class Item(models.Model):
    item_code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    sale_price = models.DecimalField(default=0, max_digits=10, decimal_places=2,help_text='(INR)')
    # purchase_price = models.DecimalField(default=0, max_digits=10, decimal_places=2,help_text='(INR)')
    description = models.TextField(blank=True, null=True)
    gst_rate = models.DecimalField(default=0, max_digits=10, decimal_places=2, help_text='(%)')
    # tds_rate = models.DecimalField(default=0, max_digits=10, decimal_places=2, help_text='(%)', null=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if self.gst_rate:
            self.gst_rate /= 100
        
        # if self.tds_rate:
        #     self.tds_rate /= 100
        super(Item, self).save(*args, **kwargs)


class InvoiceItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='invoice_items')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_items')
    quantity = models.IntegerField(default=1)
    # rate = models.DecimalField(default=0, max_digits=10, decimal_places=2,help_text='(INR)')
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    # total_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.invoice.invoice_no}"

    def save(self, *args, **kwargs):
        self.amount = self.quantity*self.item.sale_price
        self.tax_amount = self.item.gst_rate*self.item.sale_price
        # self.total_amount = self.amount + self.tax_amount
        super(InvoiceItem, self).save(*args, **kwargs)


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment = models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.invoice.invoice_no}"    







