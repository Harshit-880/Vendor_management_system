from django.db import models
from django.db.models import JSONField

class Vendor(models.Model):
    name = models.CharField(max_length=100)  
    contact_details = models.TextField()  
    address = models.TextField()  
    vendor_code = models.CharField(max_length=20, unique=True)  
    on_time_delivery_rate = models.FloatField(default=0.0)  
    quality_rating_avg = models.FloatField(default=0.0) 
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.name



class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)  
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)  
    order_date = models.DateTimeField()  
    delivery_date = models.DateTimeField()  
    items = JSONField()  
    quantity = models.IntegerField()  
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])  
    quality_rating = models.FloatField(null=True, blank=True)  
    issue_date = models.DateTimeField()  
    acknowledgment_date = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)  
    date = models.DateTimeField(auto_now_add=True)  
    on_time_delivery_rate = models.FloatField(default=0.0, null=True)  
    quality_rating_avg = models.FloatField(default=0.0, null=True)  
    average_response_time = models.FloatField(default=0.0, null=True)  
    fulfillment_rate = models.FloatField(default=0.0, null=True)  
    
    def __str__(self):
        return f"{self.vendor.name} - {self.date.strftime('%Y-%m-%d')}"
