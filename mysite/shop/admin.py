from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category', 'status', 'brand')
    list_display_links = ('id', 'title', 'price', 'category')
    prepopulated_fields = {'slug': ('title',)}


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Tag)
admin.site.register(Rubric, MPTTModelAdmin)
admin.site.register(Brand, BrandAdmin)