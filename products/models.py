from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

from django.shortcuts import reverse

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.PositiveIntegerField(default=50000)
    image = models.ImageField(verbose_name=_('Product Image'), upload_to='product/product_cover', blank=True,)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])


class ActiveCommentManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentManager, self).get_queryset().filter(active=True)


class Comment(models.Model):

    PRODUCT_STARS = [
        ('1', _('Very Bad')),
        ('2', _('Bad')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect')),
    ]

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', verbose_name='comment author')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments',)
    body = models.TextField(verbose_name=_('Comment Text'))
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name=_('What is the score?'))

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    #Manger
    objects = models.Manager()
    active_comments_manager = ActiveCommentManager()

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.product.id])
