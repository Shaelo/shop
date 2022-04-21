from django.contrib import admin

# Register your models here.
from applications.product.models import *

admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Rating)



class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ('image', )
    max_num = 5

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInAdmin
    ]
