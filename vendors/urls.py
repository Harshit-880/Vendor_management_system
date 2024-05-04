from django.urls import path
from .views import *

urlpatterns = [
    path('vendor/', VendorCreateView.as_view()),
    path('vendors/', VendorListView.as_view()),
    path('vendors/<int:vendor_id>/', VendorView.as_view()),
    path('vendors/<int:vendor_id>/delete/', VendorDelete.as_view()),
    path('vendors/<int:vendor_id>/update/', VendorUpdateView.as_view()),

    path('purchase_orders/', poCresteview.as_view()),
    path('purchase_order/<int:po_id>/update/', PurchaseOrederUpdateView.as_view()),
    path('purchase_order/', PurchaseOrderListView.as_view()),
    path('purchase_order/<int:po_id>/', PurchaseOrderView.as_view()),
    path('purchase_order/<int:po_id>/delete/', PurchaseOrderDelete.as_view()),

    path('vendors/<int:perform_id>/performance/', PerformanceView.as_view()),
]
