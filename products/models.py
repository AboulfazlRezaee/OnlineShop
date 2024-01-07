from django.db import models

from django.shortcuts import reverse

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.PositiveIntegerField(default=50000)
    active = models.BooleanField(default=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])
