from django.db import models
from django.db.models import JSONField

class Vendor(models.Model):
    name = models.CharField(max_length=100)  # Vendor's name
    contact_details = models.TextField()  # Vendor's contact details
    address = models.TextField()  # Vendor's address
    vendor_code = models.CharField(max_length=20, unique=True)  # Unique vendor code
    
    # Performance metrics
    on_time_delivery_rate = models.FloatField(default=0.0)  # Percentage of on-time deliveries
    quality_rating_avg = models.FloatField(default=0.0)  # Average quality rating
    average_response_time = models.FloatField(default=0.0)  # Average response time
    fulfillment_rate = models.FloatField(default=0.0)  # Fulfillment rate
    
    def __str__(self):
        return self.name



class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)  # Unique PO number
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)  # Link to Vendor model
    order_date = models.DateTimeField()  # Order date
    delivery_date = models.DateTimeField()  # Expected/actual delivery date
    items = JSONField()  # Details of items ordered
    quantity = models.IntegerField()  # Total quantity of items in the PO
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])  # PO status
    quality_rating = models.FloatField(null=True, blank=True)  # Quality rating given to the vendor (nullable)
    issue_date = models.DateTimeField()  # Date PO was issued
    acknowledgment_date = models.DateTimeField(null=True, blank=True)  # Date the vendor acknowledged the PO (nullable)
    
    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)  # Link to Vendor model
    date = models.DateTimeField(auto_now_add=True)  # Date of the performance record
    on_time_delivery_rate = models.FloatField(default=0.0, null=True)  # Historical record of on-time delivery rate
    quality_rating_avg = models.FloatField(default=0.0, null=True)  # Historical record of quality rating average
    average_response_time = models.FloatField(default=0.0, null=True)  # Historical record of average response time
    fulfillment_rate = models.FloatField(default=0.0, null=True)  # Historical record of fulfillment rate
    
    def __str__(self):
        return f"{self.vendor.name} - {self.date.strftime('%Y-%m-%d')}"
