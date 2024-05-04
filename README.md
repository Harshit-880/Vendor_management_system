# Vendor Management System

## Project Description
This project is a Vendor Management System using Django and Django REST Framework. It allows you to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Installation
1. **Prerequisites**:
    - Python 3.x
    - Django
    - Django REST Framework
    
2. **Setup**:
    - Clone the repository:
        ```shell
        git clone https://github.com/your_username/your_project.git
        ```
    - Navigate to the project directory:
        ```shell
        cd your_project
        ```
    - Install dependencies:
        ```shell
        pip install -r requirements.txt
        ```
    - Set up the database (migrate):
        ```shell
        python manage.py migrate
        ```
    - Create a superuser (optional):
        ```shell
        python manage.py createsuperuser
        ```

## Usage
- To run the server:
    ```shell
    python manage.py runserver
    ```

## API Endpoints
### Vendor Management
- `POST /api/vendor/`: Create a new vendor.
    Required_fields_example :
    {
    "name": "rahul",
    "contact_details": "your_details",
    "address": "your_address",
    "vendor_code": "qwertyu"
}

- `GET /api/vendors/`: List all vendors.
- `GET /api/vendors/{vendor_id}/`: Retrieve vendor details.
- `PATCH /api/vendors/{vendor_id}/update/`: Update vendor details.
Required_fields_example :
    {
    "name": "rahul",
    "contact_details": "your_details",
    "address": "your_address",
    "vendor_code": "qwertyu"
}
- `DELETE /api/vendors/{vendor_id}/delete/`: Delete a vendor.

### Purchase Order Tracking
- `POST /api/purchase_orders/`: Create a purchase order.
Required_fields_example :
{
    "po_number": "PO123455",
    "vendor": 2,  
    "order_date": "2024-05-05T12:00:00Z",
    "delivery_date": "2024-05-10T12:00:00Z",
    "items": [
        {
            "name": "Item A",
            "description": "Description of Item A",
            "quantity": 10,
            "price": 15.50
        },
        {
            "name": "Item B",
            "description": "Description of Item B",
            "quantity": 5,
            "price": 25.00
        }
    ],
    "quantity": 15,
    "status": "pending",
    "issue_date": "2024-05-05T12:00:00Z",
    "quality_rating": null,
    "acknowledgment_date": null
}

- `GET /api/purchase_order/`: List all purchase orders.
- `GET /api/purchase_order/{po_id}/`: Retrieve purchase order details.
- `PATCH /api/purchase_order/{po_id}/update/`: Update a purchase order.
Required_fields_example :
{
    "delivery_date": "2024-05-20T12:00:00Z",  Updated delivery date
    "items": [
        {
            "name": "Item A",
            "description": "Updated description of Item A",
            "quantity": 12,
            "price": 15.50
        },
        {
            "name": "Item B",
            "description": "Description of Item B",
            "quantity": 5,
            "price": 25.00
        }
    ],
    "quantity": 17,  // Updated total quantity
    "status": "completed",  // Updated status
    "quality_rating": 4.5,  // Updated quality rating
    "acknowledgment_date": "2024-05-03T17:00:00Z"  // Updated acknowledgment date
}

- `DELETE /api/purchase_order/{po_id}/delete/`: Delete a purchase order.

### Vendor Performance Evaluation
- `GET /api/vendors/{vendor_id}/performance/`: Retrieve performance metrics.

## Data Models
### Vendor Model
- `name`: Vendor's name.
- `contact_details`: Contact information of the vendor.
- `address`: Physical address of the vendor.
- `vendor_code`: Unique identifier for the vendor.
- `on_time_delivery_rate`: Percentage of on-time deliveries (as a percentage).
- `quality_rating_avg`: Average quality rating based on purchase orders.
- `average_response_time`: Average time taken to acknowledge purchase orders.
- `fulfillment_rate`: Percentage of fulfilled purchase orders (as a percentage).

### Purchase Order Model
- `po_number`: Unique number identifying the purchase order.
- `vendor`: Reference to the vendor (ForeignKey).
- `order_date`: Date when the order was placed.
- `delivery_date`: Expected or actual delivery date of the order.
- `items`: Details of items ordered (JSONField).
- `quantity`: Total quantity of items in the purchase order.
- `status`: Current status of the purchase order (e.g., pending, completed, canceled).
- `quality_rating`: Rating given to the vendor for this purchase order (nullable).
- `issue_date`: Timestamp when the purchase order was issued.
- `acknowledgment_date`: Timestamp when the vendor acknowledged the purchase order (nullable).

### Historical Performance Model
- `vendor`: Reference to the vendor (ForeignKey).
- `date`: Date of the performance record.
- `on_time_delivery_rate`: Historical on-time delivery rate.
- `quality_rating_avg`: Historical quality rating average.
- `average_response_time`: Historical average response time.
- `fulfillment_rate`: Historical fulfillment rate.

## Performance Metrics
- **On-Time Delivery Rate**: Percentage of orders delivered on time.
- **Quality Rating Average**: Average rating given to vendors based on purchase orders.
- **Average Response Time**: Average time taken by the vendor to acknowledge or respond to purchase orders.
- **Fulfillment Rate**: Percentage of purchase orders fulfilled without issues.

## Features
- Manage vendor profiles.
- Track purchase orders and their details.
- Evaluate vendor performance metrics such as on-time delivery rate and fulfillment rate.
- API endpoints to interact with the system.

