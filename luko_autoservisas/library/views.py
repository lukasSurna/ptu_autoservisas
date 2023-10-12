from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models.query import QuerySet, Q
from . import models, forms


class AddCarView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'library/add_car.html'
    form_class = forms.AddCarForm

    def form_valid(self, form):
        car_model, created = models.CarModel.objects.get_or_create(
            brand=form.cleaned_data['brand'],
            model=form.cleaned_data['model'],
            year=form.cleaned_data['year']
        )
        new_car = models.Car(
            customer=self.request.user,
            car_model=car_model,
            plate=form.cleaned_data['plate'],
            vin=form.cleaned_data['vin'],
            color=form.cleaned_data['color']
        )
        new_car.save()

        return redirect('user_car_list')


class PlaceOrderView(generic.edit.FormView):
    template_name = 'library/order_form.html'
    form_class = forms.OrderForm

    def form_valid(self, form):
        car_id = self.kwargs['car_id']
        car = get_object_or_404(models.Car, pk=car_id)
        part_service = form.cleaned_data['part_service']
        quantity = form.cleaned_data['quantity']
        cancel_order = form.cleaned_data.get('cancel_order')

        if cancel_order:
            service_order = models.ServiceOrder.objects.create(
                car=car, status=3 
            )
            messages.success(self.request, 'Order canceled successfully.')
        else:
            service_order = models.ServiceOrder.objects.create(car=car)

            models.OrderLine.objects.create(
                order=service_order,
                part_service=part_service,
                quantity=quantity,
                price=part_service.price * quantity,
            )

            messages.success(self.request, 'Order placed successfully.')
        
        return redirect('user_car_list')


class CarServiceOrderListView(LoginRequiredMixin, generic.ListView):
    model = models.ServiceOrder
    template_name = 'library/serviceorder_list.html'
    context_object_name = 'service_orders'

    def get_queryset(self):
        customer = self.request.user
        car = get_object_or_404(models.Car, pk=self.kwargs['car_id'])
        return models.ServiceOrder.objects.filter(car=car, car__customer=customer)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = get_object_or_404(models.Car, pk=self.kwargs['car_id'])
        context['car'] = car
        context['date'] = models.ServiceOrder.objects.filter(car=car, car__customer=self.request.user).first().date
        return context


class UserCarListView(LoginRequiredMixin, generic.ListView):
    model = models.Car
    template_name = 'library/user_car_list.html'
    context_object_name = 'car_list'
    paginate_by = 2

    def get_queryset(self):
        user = self.request.user
        return models.Car.objects.filter(customer=user)

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


class PartServiceDetailView(generic.edit.FormMixin, generic.DetailView):
    model = models.PartService
    template_name = 'library/part_detail.html'
    context_object_name = 'partservice'
    form_class = forms.PartServiceReviewForm

    def get_initial(self):
        initial = super().get_initial()
        initial['partservice'] = self.get_object()
        initial['reviewer'] = self.request.user
        return initial

    def post(self, *args, **kwargs) ->HttpResponse:
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form) -> HttpResponse:
        form.instance.partservice = self.object
        form.instance.reviewer = self.request.user
        form.save()
        messages.success(self.request, 'Review added successfully.')
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('part_detail', kwargs={'pk': self.object.pk})


def cancel_order(request, order_id):
    order = get_object_or_404(models.ServiceOrder, pk=order_id)
    if order.order_status == 0:
        order.order_status = 2
        order.save()
        messages.success(request, 'Order canceled successfully')
    else:
        messages.error(request, 'Something wrong')
    return redirect('serviceorder_list')

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

# def part_detail(request:HttpRequest, pk:int):
#     return render(
#         request,
#         'library/part_detail.html',
#         {'part': get_object_or_404(models.PartService, pk=pk)}
#     )

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

def review_create(request: HttpRequest):
    if request.method == 'POST':
        form = forms.PartServiceReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.save()
            messages.success(request, 'Review added successfully.')
            return redirect('part_detail', pk=review.partservice.pk)
    else:
        form = forms.PartServiceReviewForm()

    return render(request, 'partservice_review_create.html', {'form': form})