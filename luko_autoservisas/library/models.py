from datetime import date
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

User = get_user_model()


class CarModel(models.Model):
    brand = models.CharField(_("brand"), max_length=50, db_index=True)
    model = models.CharField(_("model"), max_length=50, db_index=True)     
    year = models.PositiveIntegerField(_("year"))

    class Meta:
        verbose_name = _("car model")
        verbose_name_plural = _("car models")
        ordering = ['brand', 'model']

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"

    def get_absolute_url(self):
        return reverse("car_model_detail", kwargs={"pk": self.pk})
    

class Car(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("customer"))
    car_model = models.ForeignKey(
        CarModel, 
        verbose_name=_("car model"),
        on_delete=models.CASCADE,
        related_name='cars',
    )
    plate = models.CharField(_("plate"), max_length=6, db_index=True)
    vin = models.CharField(_("vin"), max_length=17)
    color = models.CharField(_("color"), max_length=20)

    class Meta:
        verbose_name = _("car")
        verbose_name_plural = _("cars")
        ordering = ['customer', 'plate']

    def __str__(self):
        return f"{self.customer}, {self.car_model}, {self.plate}, {self.vin}, {self.color}"

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})
    

ORDER_STATUS = (
    (0, _('pending')),
    (1, _('awaiting payment')),
    (2, _('cancelled')),
    (3, _('declined')),
    (4, _('completed')),
)


class ServiceOrder(models.Model):
    car = models.ForeignKey(Car, 
    verbose_name=_("car"), 
    on_delete=models.CASCADE,
    related_name='orders',
    db_index=True,
    null=False
    )
    date = models.DateField(_("date"), auto_now=True, db_index=True)
    order_status = models.PositiveSmallIntegerField(
        _("status"), choices=ORDER_STATUS, default=0,
    )

    class Meta:
        verbose_name = _("service_order")
        verbose_name_plural = _("service_orders")
        ordering = ['car']

    def __str__(self):
        return f"{self.car} {self.date}"

    def get_absolute_url(self):
        return reverse("service_order_detail", kwargs={"pk": self.pk})
    
    @property
    def is_overdue(self):
        if self.due_back and self.due_back < date.today():
            return True
        return False
    

class PartService(models.Model):
    name = models.CharField(_("name"), max_length=50, db_index=True)
    price = models.DecimalField(_("price"), max_digits=12, decimal_places=2)
    description = models.TextField(_("Description"), max_length=4000, default='', blank=True)
    cover = models.ImageField(_('nopart'), upload_to='part_covers', null=True, blank=True)

    class Meta:
        verbose_name = _("part_service")
        verbose_name_plural = _("part_services")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} {self.price}"

    def get_absolute_url(self):
        return reverse("part_service_detail", kwargs={"pk": self.pk})


class OrderLine(models.Model):
    order = models.ForeignKey(
        ServiceOrder, 
        verbose_name=_("order"), 
        on_delete=models.CASCADE,
        related_name='lines',
        db_index=True,
    )
    part_service = models.ForeignKey(
        PartService, 
        verbose_name=_("part service"), 
        on_delete=models.CASCADE,
        related_name='lines',
    )
    quantity = models.IntegerField(_("quantity"), default=1)
    price = models.DecimalField(_("price"), max_digits=12, decimal_places=2)
    

    class Meta:
        verbose_name = _("order_line")
        verbose_name_plural = _("order_lines")
        ordering = ['order']

    def __str__(self):
        return f"{self.order} {self.part_service} {self.quantity} {self.price}"

    def get_absolute_url(self):
        return reverse("order_line_detail", kwargs={"pk": self.pk})


class PartServiceReview(models.Model):
    partservice = models.ForeignKey(
        PartService,
        verbose_name=_("part or service"),
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    reviewer = models.ForeignKey(
        User,
        verbose_name=_("reviewer"),
        on_delete=models.CASCADE,
        related_name='part_service_reviews',
    )
    content = models.TextField(_("Content"), max_length=4000)
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = _("part or service review")
        verbose_name_plural = _("part or service reviews")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.partservice} review by {self.reviewer}"

    def get_absolute_url(self):
        return reverse("partservicereview_detail", kwargs={"pk": self.pk})