from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from .models import *



from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance, Vendor
from django.db import models


def update_vendor_performance(vendor):
    historical_data = HistoricalPerformance.objects.filter(vendor=vendor)
    total_entries = historical_data.count()
    
    if total_entries > 0:
        vendor.on_time_delivery_rate = historical_data.aggregate(models.Avg('on_time_delivery_rate'))['on_time_delivery_rate__avg'] or 0.0
        vendor.quality_rating_avg = historical_data.aggregate(models.Avg('quality_rating_avg'))['quality_rating_avg__avg'] or 0.0
        
        vendor.average_response_time = historical_data.aggregate(models.Avg('average_response_time'))['average_response_time__avg'] or 0.0
        
        vendor.fulfillment_rate = historical_data.aggregate(models.Avg('fulfillment_rate'))['fulfillment_rate__avg'] or 0.0
        
        vendor.on_time_delivery_rate *= 100
        vendor.fulfillment_rate *= 100

    else:
        vendor.on_time_delivery_rate = 0.0
        vendor.quality_rating_avg = 0.0
        vendor.average_response_time = 0.0
        vendor.fulfillment_rate = 0.0

    
    vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_historical_performance(sender, instance, created, **kwargs):
    """Signal handler to update historical performance data when a purchase order is created or updated."""
    purchase_order = instance
    vendor = purchase_order.vendor
    try:
        historical_performance = HistoricalPerformance.objects.get(vendor=vendor)
    except HistoricalPerformance.DoesNotExist:
        historical_performance = HistoricalPerformance(vendor=vendor)

    total_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    
    if purchase_order.status == 'completed':
        on_time_deliveries = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            delivery_date__lte=purchase_order.expected_delivery_date
        ).count()
        historical_performance.on_time_delivery_rate = on_time_deliveries / total_completed_orders if total_completed_orders > 0 else 0.0

    if purchase_order.status == 'completed' and purchase_order.quality_rating is not None:
        quality_ratings = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed', quality_rating__isnull=False
        ).values_list('quality_rating', flat=True)
        historical_performance.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0.0

    if purchase_order.acknowledgment_date:
        response_times = PurchaseOrder.objects.filter(
            vendor=vendor, acknowledgment_date__isnull=False
        ).annotate(response_time=models.ExpressionWrapper(
            models.F('acknowledgment_date') - models.F('issue_date'),
            output_field=models.DurationField()
        )).values_list('response_time', flat=True)
        historical_performance.average_response_time = sum(response_times) / len(response_times) if response_times else 0.0

    if purchase_order.status == 'completed':
        fulfilled_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        
        historical_performance.fulfillment_rate = fulfilled_orders / len(PurchaseOrder.objects.filter(vendor=vendor)) if len(PurchaseOrder.objects.filter(vendor=vendor)) > 0 else 0.0

    historical_performance.save() 
    update_vendor_performance(vendor)
