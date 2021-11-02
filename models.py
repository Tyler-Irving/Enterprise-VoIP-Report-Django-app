from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FilteredRateCentersModel(models.Model):
    value = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.value, self.description}'

class QueryInfoModel(models.Model):
    location = models.TextField(default="none", null=True)
    number_status = models.TextField(default="none", null=True)
    port_in = models.TextField(null=True)
    rate_center = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

class NumberStatusModel(models.Model):
    value = models.TextField(null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.value} - {self.description}'

class ServiceLocationModel(models.Model):
    service_location_value = models.TextField(default="none", null=True)
    service_location_description = models.TextField(default="none", null=True)

    def __str__(self):
        return f"{self.service_location_value, self.service_location_description}"

class DisplayModel(models.Model):
    service_location = models.TextField(null=True)
    rate_center = models.TextField(null=True)
    number_status = models.TextField(null=True)
    phone_number = models.TextField(null=True)
    port_in = models.TextField(null=True)
    act_date = models.TextField(null=True)
    deact_date = models.TextField(null=True)
    returned_date = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.service_location
