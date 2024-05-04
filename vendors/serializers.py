from rest_framework import serializers
from .models import *


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code']

    def create(self, validated_data):
        vendor = Vendor.objects.create(**validated_data)
        return vendor

class VendorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields='__all__'



class VendorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code']

    def update(self, instance, validated_data):
        
        instance.name = validated_data.get('name', instance.name)
        instance.contact_details = validated_data.get('contact_details', instance.contact_details)
        instance.address = validated_data.get('address', instance.address)
        instance.vendor_code = validated_data.get('vendor_code', instance.vendor_code)
        
        # Save the instance to apply the updates
        instance.save()
        
        # Return the updated instance
        return instance

class PurchaseOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields='__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields='__all__'


class PurchaseOrederUpdate(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields=['delivery_date','items','quantity','status','quality_rating','acknowledgment_date']

    def update(self, instance, validated_data):
        
        instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
        instance.items = validated_data.get('items', instance.items)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.quality_rating = validated_data.get('quality_rating', instance.quality_rating)
        instance.acknowledgment_date = validated_data.get('acknowledgment_date', instance.acknowledgment_date)
        
        # Save the instance to apply the updates
        instance.save()
        
        # Return the updated instance
        return instance
    

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields='__all__'