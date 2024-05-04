from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from .models import *


# @receiver(post_save, sender=PurchaseOrder)
# def update_historical_performance(sender, instance, **kwargs):
#     print("vendor")
#     purchase_order = instance
#     vendor = purchase_order.vendor
    
#     # Calculate performance metrics from the purchase order
#     # Example: Calculate on-time delivery rate, quality rating average, average response time, fulfillment rate
#     # For simplicity, the example assumes single historical performance entry for the vendor.
#     # You may need more complex aggregation logic based on your application's requirements.

#     # Create or get the HistoricalPerformance instance
#     historical_performance, created = HistoricalPerformance.objects.get_or_create(
#         vendor=vendor,
#         date=purchase_order.order_date.date()  # Use order date as historical date for simplicity
#     )

#     # Update performance metrics based on the purchase order
#     # Example calculations: Modify as per your data and metrics calculation logic
#     if purchase_order.status == 'completed':
#         if purchase_order.delivery_date <= purchase_order.delivery_date:
#             historical_performance.on_time_delivery_rate += 1
        
#         historical_performance.on_time_delivery_rate /= len(PurchaseOrder.objects.filter(vendor=vendor, status='completed'))

#     if purchase_order.quality_rating is not None:
#         historical_performance.quality_rating_avg += purchase_order.quality_rating
#         historical_performance.quality_rating_avg /= len(PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False))

#     if purchase_order.acknowledgment_date:
#         response_time = (purchase_order.acknowledgment_date - purchase_order.issue_date).total_seconds()
#         historical_performance.average_response_time += response_time
#         historical_performance.average_response_time /= len(PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False))

#     if purchase_order.status == 'completed':
#         historical_performance.fulfillment_rate += 1
#         historical_performance.fulfillment_rate /= len(PurchaseOrder.objects.filter(vendor=vendor))

#     # Save the historical performance data
#     historical_performance.save()


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance, Vendor
from django.db import models


def update_vendor_performance(vendor):
    """Update the vendor's performance metrics based on historical data."""
    # Aggregate historical data for the vendor
    historical_data = HistoricalPerformance.objects.filter(vendor=vendor)

    # Calculate and update vendor's performance metrics
    total_entries = historical_data.count()
    
    if total_entries > 0:
        # Calculate on-time delivery rate as a percentage
        vendor.on_time_delivery_rate = historical_data.aggregate(models.Avg('on_time_delivery_rate'))['on_time_delivery_rate__avg'] or 0.0
        
        # Calculate quality rating average
        vendor.quality_rating_avg = historical_data.aggregate(models.Avg('quality_rating_avg'))['quality_rating_avg__avg'] or 0.0
        
        # Calculate average response time
        vendor.average_response_time = historical_data.aggregate(models.Avg('average_response_time'))['average_response_time__avg'] or 0.0
        
        # Calculate fulfillment rate as a percentage
        vendor.fulfillment_rate = historical_data.aggregate(models.Avg('fulfillment_rate'))['fulfillment_rate__avg'] or 0.0
        
        # Convert rates to percentages
        vendor.on_time_delivery_rate *= 100
        vendor.fulfillment_rate *= 100

    else:
        # If there is no historical data, set metrics to 0
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
    
    # Retrieve the HistoricalPerformance instance for the vendor
    try:
        historical_performance = HistoricalPerformance.objects.get(vendor=vendor)
    except HistoricalPerformance.DoesNotExist:
        # Create a new HistoricalPerformance instance if it does not exist (though it should be unique)
        historical_performance = HistoricalPerformance(vendor=vendor)

    # Calculate the new performance metrics
    total_completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    
    # On-Time Delivery Rate:
    if purchase_order.status == 'completed':
        on_time_deliveries = PurchaseOrder.objects.filter(
            vendor=vendor,
            status='completed',
            delivery_date__lte=purchase_order.expected_delivery_date
        ).count()
        # Calculate average on-time delivery rate
        historical_performance.on_time_delivery_rate = on_time_deliveries / total_completed_orders if total_completed_orders > 0 else 0.0

    # Quality Rating Average:
    if purchase_order.status == 'completed' and purchase_order.quality_rating is not None:
        quality_ratings = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed', quality_rating__isnull=False
        ).values_list('quality_rating', flat=True)
        # Calculate average quality rating
        historical_performance.quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0.0

    # Average Response Time:
    if purchase_order.acknowledgment_date:
        # Calculate average response time
        response_times = PurchaseOrder.objects.filter(
            vendor=vendor, acknowledgment_date__isnull=False
        ).annotate(response_time=models.ExpressionWrapper(
            models.F('acknowledgment_date') - models.F('issue_date'),
            output_field=models.DurationField()
        )).values_list('response_time', flat=True)
        historical_performance.average_response_time = sum(response_times) / len(response_times) if response_times else 0.0

    # Fulfillment Rate:
    if purchase_order.status == 'completed':
        fulfilled_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        # Calculate average fulfillment rate
        historical_performance.fulfillment_rate = fulfilled_orders / len(PurchaseOrder.objects.filter(vendor=vendor)) if len(PurchaseOrder.objects.filter(vendor=vendor)) > 0 else 0.0

    # Save the updated historical performance data
    historical_performance.save() 

    # Call the function to update vendor's performance metrics based on the historical data
    update_vendor_performance(vendor)
