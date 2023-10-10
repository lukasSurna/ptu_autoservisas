from typing import Any
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models.query import QuerySet, Q
from . import models 


class ServiceListView(generic.ListView):
    model = models.ServiceOrder
    template_name = 'service_list.html'
    context_object_name = 'service_orders'
    paginate_by = 1 #kiek irasu rodyti puslapyje
 
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['search'] = True
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset =  super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                Q(pk__icontains=query) |
                Q(date__icontains=query) |
                Q(car__customer__istartswith=query) |
                Q(lines__part_service__name__icontains=query)
            )
        return queryset

def index(request: HttpRequest):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_carModel': models.CarModel.objects.count(),
        'brands': models.CarModel.objects.values_list('brand', flat=True).distinct(),
        'parts': models.PartService.objects.count(),
        'orders': models.ServiceOrder.objects.count(),
        'completed_orders': models.ServiceOrder.objects.filter(order_status=4).count(),
        'num_visits': num_visits
    }
    return render(request, 'library/index.html', context)

def parts(request: HttpRequest):
    part_pages = Paginator(models.PartService.objects.all(), 2) #kiek irasu rodyti puslapyje
    current_page = request.GET.get('page') or 1
    return render(
        request,
        'library/part_list.html',
        {'part_list': part_pages.get_page(current_page)},
    )

def part_detail(request:HttpRequest, pk:int):
    return render(
        request,
        'library/part_detail.html',
        {'part': get_object_or_404(models.PartService, pk=pk)}
    )

def brand_list(request: HttpRequest):
    return render(
        request,
        'library/brand_list.html',
        {'brand_list': models.CarModel.objects.all()},
    )

def brand_detail(request: HttpRequest, pk:int):
    return render(
        request,
        'library/brand_detail.html',
        {'brand': get_object_or_404(models.CarModel, pk=pk)},
    )


def customer_list(request: HttpRequest):
    customers = models.Car.objects.all()
    return render(request, 'library/customer_list.html', {'customers': customers})

def customer_detail(request: HttpRequest, pk:int):
    customer = get_object_or_404(models.Car, pk=pk)
    cars = models.Car.objects.filter(car_model=customer.car_model)
    return render(request, 'library/customer_detail.html', {'customer': customer, 'cars': cars})
