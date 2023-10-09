from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('parts/', views.parts, name='part_list'),
    path('parts/<int:pk>/', views.part_detail, name='part_detail'),
    path('brands/', views.brand_list, name='brand_list'),
    path('brand/<int:pk>/', views.brand_detail, name='brand_detail'),
    path('customers/', views.customer_list, name='customer_list'),  
    path('customer/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('service/', views.ServiceListView.as_view(), name='service_list'),
]
