from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('test/', test, name='test'),
    path('category/', CategoryPage.as_view(), name='cat'),
    path('filter/', FilterProducts.as_view(), name='filter'),
    path('category/<slug:category_slug>/', CategoryPageView.as_view(), name='category'),
    path('product/<slug:product_slug>/', ProductPageView.as_view(), name='product'),
    path('add/', AddPage.as_view(), name='add_page'),
    path('edit/<slug:slug>/', ProductEditPage.as_view(), name='edit_page'),
    path('search/', SearchProducts.as_view(), name='search')

]