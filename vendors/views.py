
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import *

class VendorCreateView(APIView):
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorListView(ListAPIView):
    serializer_class = VendorListSerializer

    def get_queryset(self):
        return Vendor.objects.all()


class VendorView(ListAPIView):
    serializer_class = VendorListSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('vendor_id')
        if not user_id:
            raise ValidationError("User profile not found for the given user_id")
        vendor = get_object_or_404(Vendor, id = user_id)
        serialized_vendor = self.serializer_class(vendor)
        return Response(serialized_vendor.data, status=status.HTTP_200_OK)


class VendorDelete(APIView):
    def delete(self, request, *args, **kwargs):
        vendor_id = kwargs.get('vendor_id')
        if not vendor_id:
            return Response({"error": "Vendor ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the vendor object using vendor_id
        vendor = get_object_or_404(Vendor, id=vendor_id)

        # Delete the vendor instance
        vendor.delete()

        # Return a successful response
        return Response({"message": "Vendor deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class VendorUpdateView(APIView):
    def patch(self, request, *args, **kwargs):
        vendor_id = kwargs.get('vendor_id')
        vendor = get_object_or_404(Vendor, id=vendor_id)
        
        # Create a serializer instance with the Vendor instance and request data
        serializer = VendorUpdateSerializer(vendor, data=request.data, partial=True)
        
        # Validate the request data using the serializer
        if serializer.is_valid():
            # Save the updated Vendor instance using the serializer
            serializer.save()
            
            # Return the updated Vendor instance serialized
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Return validation errors if the request data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class  poCresteview(APIView):
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PurchaseOrederUpdateView(APIView):
    def patch(self, request, *args, **kwargs):
        purchase_id = kwargs.get('vendor_id')
        PO = get_object_or_404(PurchaseOrder, id=purchase_id)
        
        # Create a serializer instance with the Vendor instance and request data
        serializer = PurchaseOrederUpdate(PO, data=request.data, partial=True)
        
        # Validate the request data using the serializer
        if serializer.is_valid():
            # Save the updated Vendor instance using the serializer
            serializer.save()
            
            # Return the updated Vendor instance serialized
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Return validation errors if the request data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderListView(ListAPIView):
    serializer_class = PurchaseOrderListSerializer

    def get_queryset(self):
        # Get the vendor_id from the request query parameters
        vendor_id = self.request.query_params.get('vendor_id', None)
        
        # Start with all PurchaseOrder objects
        queryset = PurchaseOrder.objects.all()

        # If vendor_id is provided in the query params, filter the queryset
        if vendor_id:
            queryset = queryset.filter(vendor__id=vendor_id)
        
        return queryset
    

class PurchaseOrderView(ListAPIView):
    serializer_class = PurchaseOrderSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('po_id')
        if not user_id:
            raise ValidationError("po not found for the given user_id")
        purchaseOrder = get_object_or_404(PurchaseOrder, id = user_id)
        serialized_po = self.serializer_class(purchaseOrder)
        return Response(serialized_po.data, status=status.HTTP_200_OK)
    

class PurchaseOrderDelete(APIView):
    def delete(self, request, *args, **kwargs):
        po_id = kwargs.get('po_id')
        if not po_id:
            return Response({"error": "purchase order not exist not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the vendor object using vendor_id
        po = get_object_or_404(PurchaseOrder, id=po_id)

        # Delete the vendor instance
        if po.status == 'completed':
            return Response({"message": "Purchase Order cannot be deleted ."}, status=status.HTTP_204_NO_CONTENT)
        
        po.delete()
        # Return a successful response
        return Response({"message": "Purchase Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class PerformanceView(APIView):
    serializer_class = PerformanceSerializer

    def get(self, request, *args, **kwargs):
        perf_id = kwargs.get('perform_id')
        if not perf_id:
            raise ValidationError("User profile not found for the given user_id")
        performance = get_object_or_404(HistoricalPerformance, vendor = perf_id)
        serialized_vendor = self.serializer_class(performance)
        return Response(serialized_vendor.data, status=status.HTTP_200_OK)