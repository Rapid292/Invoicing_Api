from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invoice, Payment

@receiver(post_save, sender=Payment)
def update_pending_amount(sender, instance, created, **kwargs):
    print("Rapid..........................................................")
    if created:
        Invoice.objects.update()
        # invoice = instance.invoice
        # invoice_pending_amount = Invoice.objects.get(invoice = invoice).pending_amount
        # if invoice_pending_amount > instance.payment:
        #     invoice_pending_amount -= instance.payment
        #     Invoice.objects.update(pending_amount=invoice_pending_amount)


@receiver(post_save, sender=Payment)
def save_invoice(sender, instance, **kwargs):
    print("Rishabh..........................................................")
    instance.invoice.save()