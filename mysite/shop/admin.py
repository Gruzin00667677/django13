from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from mptt.admin import MPTTModelAdmin


# Register your models here.
class GalleryInline(admin.TabularInline):
    model = Gallery
    fk_name = 'product'
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'get_products_count')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_products_count.short_description = 'Кол-во'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category', 'status', 'brand', 'get_html_photo')
    list_display_links = ('id', 'title', 'price', 'category')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'brand')
    save_as = True
    inlines = (GalleryInline,)

    def get_html_photo(self, obj):
        if obj.images.all():
            return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width=50>')

    get_html_photo.short_description = 'Фото'


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}






admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Tag)
admin.site.register(Rubric, MPTTModelAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Gallery)