from django.contrib import admin
from rango.models import Category, Page

# Register your models here.

class PageAdmin(admin.ModelAdmin):
    list_display = 'title', 'category', 'url'
    list_filter = ['title']
    search_fields = ['category']

admin.site.register(Category)
admin.site.register(Page, PageAdmin)
