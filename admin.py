from django.contrib import admin
from .models import ServiceLocationModel, QueryInfoModel, NumberStatusModel, FilteredRateCentersModel, DisplayModel
# Register your models here.

admin.site.register(ServiceLocationModel)
admin.site.register(QueryInfoModel)
admin.site.register(NumberStatusModel)
admin.site.register(FilteredRateCentersModel)
admin.site.register(DisplayModel)