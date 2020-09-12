# from django.http.response import HttpResponse
from .models import Invoice, InvoiceItem, Payment
from .serializers import InvoiceSerializer, InvoiceItemSerializer, PaymentSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class InvoiceAPIView(APIView):

    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
        

class InvoiceDetails(APIView):
    def get_object(self, id):
        try:
            return Invoice.objects.get(id=id)
        except InvoiceItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        invoice = self.get_object(id)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)


    def put(self, request, id):
        invoice = self.get_object(id)
        serializer = InvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
        
    def delete(self, request, id):
        invoice = self.get_object(id)
        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InvoiceItemDetails(APIView):
    
    def get_object(self, id):
        try:
            return InvoiceItem.objects.filter(invoice = id)

        except InvoiceItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):

        invoice_items = self.get_object(id)
        serializer = InvoiceItemSerializer(invoice_items, many=True)
        return Response(serializer.data)

    
    def post(self, request, id):
        serializer = InvoiceItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    
    def put(self, request, id):
        invoice_items = self.get_object(id)
        serializer = InvoiceSerializer(invoice_items, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
        
    def delete(self, request, id):
        invoice_items = self.get_object(id)
        invoice_items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentDetails(APIView):
    def get_object(self, id):
        try:
            return Payment.objects.filter(invoice = id)

        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    # def get_invoice_object(self, id):
    #     return Invoice.objects.get(id=id)

    def get(self, request, id):

        payments = self.get_object(id)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    
    def post(self, request, id):
        # invoice = self.get_invoice_object(id)
        # invoice_serializer = InvoiceSerializer(invoice)
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid() :
        # and invoice_serializer.is_valid():
            serializer.save()
            # invoice_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    
    def put(self, request, id):
        invoice_items = self.get_object(id)
        serializer = PaymentSerializer(invoice_items, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
        
    def delete(self, request, id):
        invoice_items = self.get_object(id)
        invoice_items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# class InvoiceGenericApiView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
#     serializer_class = InvoiceSerializer
#     queryset = Invoice.objects.all()

#     lookup_field = 'id'

#     def get(self, request):
#         return self.list(request)

#     def post(self, request):
#         return self.create(request)

#     def put(self, request, id=None):
#         return self.update(request, id)

