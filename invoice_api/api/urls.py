from django.urls import path
from .views import InvoiceAPIView, InvoiceDetails, InvoiceItemDetails, PaymentDetails

urlpatterns = [
    path('invoices/', InvoiceAPIView.as_view()),
    path('invoice/<int:id>', InvoiceDetails.as_view()),
    path('invoice/<int:id>/items', InvoiceItemDetails.as_view()),
    path('invoice/<int:id>/payments', PaymentDetails.as_view()),

]