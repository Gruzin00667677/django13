from django import forms
from django.core.exceptions import ValidationError

from .models import Product, Category


class AddProduct(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        # fields = ['title', 'slug', 'description', 'price', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'cols': 50, 'rows': 10})
        }
        labels = {'slug': 'Ссылка'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 20:
            raise ValidationError('Длина превышает 20 символов')
        return title
