from django import forms
from . import models

class AddCarForm(forms.ModelForm):
    brand = forms.CharField(label="Brand", max_length=50)
    model = forms.CharField(label="Model", max_length=50)
    year = forms.IntegerField(label="Year")

    class Meta:
        model = models.Car
        fields = ['brand', 'model', 'year', 'plate', 'vin', 'color']

class OrderForm(forms.Form):
    part_service = forms.ModelChoiceField(
        queryset=models.PartService.objects.all(),
        label="Select Part or Service",
    )
    quantity = forms.IntegerField(min_value=1, label="Quantity")


class PartServiceReviewForm(forms.ModelForm):
    class Meta:
        model = models.PartServiceReview
        fields = ('content', 'partservice')
        widgets = {
            'partservice': forms.HiddenInput(),
        }
        labels = {
            'content': '',
        }


class PartServiceReviewForm(forms.ModelForm):
    class Meta:
        model = models.PartServiceReview
        fields = ('content', 'partservice', 'reviewer')
        widgets = {
            'partservice': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }
        labels = {
            'content': '',
        }
