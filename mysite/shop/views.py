from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView, FormView, CreateView, DetailView, UpdateView
from cart.forms import CartAddProductForm

from .forms import AddProduct
from .models import *
from .telegramm import send_message


# Create your views here.
# def index(request):
#     return render(request, 'shop/index.html')


class IndexView(ListView):
    # model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(status='PB').select_related('category')
        # return Product.objects.all()


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        message = "*ЗАЯВКА С САЙТА*:"
        send_message(message)
        return context

        # search_query = self.request.GET.get('search', 'Товары не найдены')
        # print(search_query)
        # if search_query:
        #     return Product.objects.filter(title__icontains=search_query)

        #return Product.objects.all()


# class IndexView(TemplateView):
#     template_name = 'shop/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Главная страница!'
#         context["content"] = 'Тут будет контент'
#         context['brands'] = Brand.objects.all()
#         return context


class CategoryPageView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['category_slug'])
        context['now'] = timezone.now()
        return context


class ProductPageView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    cart_product_form = CartAddProductForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Product.objects.get(slug=self.kwargs['product_slug'])
        context['cart_product_form'] = self.cart_product_form
        return context


def test(request):
    rubrics = Rubric.objects.all()
    context = {
        'rubrics': rubrics
    }
    return render(request, 'shop/test.html', context=context)


class CategoryPage(ListView):
    model = Category
    template_name = 'shop/category.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        return context


class AddPage(CreateView):
    form_class = AddProduct
    # model = Product
    # fields = '__all__'
    template_name = 'shop/add_page.html'
    # success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Добавление статьи'
    }


class ProductEditPage(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'shop/add_page.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'title': 'Редактирование страницы'
    }


# def add_page(request):
#     if request.method == 'POST':
#         form = AddProduct(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Product.objects.create(**form.cleaned_data)
#             # except:
#             #     form.add_error(None, 'Ошибка')
#             form.save()
#             return redirect('index')
#     else:
#         form = AddProduct()
#         print(form)
#     context = {
#         'title': 'Добавление статьи',
#         'form': form
#     }
#     return render(request, 'shop/add_page.html', context=context)


class FilterProducts(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    slug_url_kwarg = 'product_slug'

    def get_queryset(self):
        return Product.objects.filter(brand__in=self.request.GET.getlist('brand'))
        # queryset = Product.objects.all()


class SearchProducts(ListView):
    model = Product
    template_name = 'shop/search.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        return Product.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск'
        context['s'] = f"search={self.request.GET.get('search')}&"
        return context


def show_rubric(request, pk):
    rubrics = Rubric.objects.all()
    context = {
        'rubrics': rubrics
    }
    return render(request, 'shop/test.html', context=context)


class RubricPage(ListView):
    model = Rubric
    template_name = 'shop/rub.html'
    context_object_name = 'rubrics'

    def get_queryset(self):
        return Rubric.objects.filter(parent=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рубрики'
        return context


class RubricPageView(ListView):
    model = Rubric
    template_name = 'shop/index.html'
    context_object_name = 'rubrics'
    allow_empty = False

    def get_queryset(self):
        return Rubric.objects.filter(parent_id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Rubric.objects.get(pk=self.kwargs['pk'])
        context['now'] = timezone.now()
        return context

