
from django.contrib import admin
from django.urls import path,include
from vendors import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vendors.urls')),
]
