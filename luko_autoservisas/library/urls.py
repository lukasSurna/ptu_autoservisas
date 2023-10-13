from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('parts/', views.parts, name='part_list'),
    path('brands/', views.brand_list, name='brand_list'),
    path('brand/<int:pk>/', views.brand_detail, name='brand_detail'),
    path('customers/', views.customer_list, name='customer_list'),  
    path('customer/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('serviceorder-list/', views.ServiceListView.as_view(), name='serviceorder_list'),
    path('user_car_list/', views.UserCarListView.as_view(), name='user_car_list'),
    path('add_car/', views.AddCarView.as_view(), name='add_car'),
    path('my_cars/', views.UserCarListView.as_view(), name='my_cars'),
    path('car/<int:car_id>/service-orders/', views.CarServiceOrderListView.as_view(), name='car_service_orders'),
    path('place_order/<int:car_id>/', views.PlaceOrderView.as_view(), name='place_order'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('review/create/', views.review_create, name='review_create'),
    path('parts/<int:pk>/', views.PartServiceDetailView.as_view(), name='part_detail'),
]   
