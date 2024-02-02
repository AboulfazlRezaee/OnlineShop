from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse

from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=120, verbose_name=_('title'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Category'))
    description = RichTextField(_('Description'))
    short_description = models.TextField(_('Short Description'), max_length=500, blank=True)
    weight = models.PositiveIntegerField(_('Weight'), null=True, blank=True)
    color = models.CharField(_('Color'), max_length=100, blank=True)
    price = models.PositiveIntegerField(default=50000, verbose_name=_('current-price'))
    s_price = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_('last-price'))
    image = models.ImageField(verbose_name=_('Product Image'), upload_to='product/product_cover', blank=True,)

    datetime_created = models.DateTimeField(default=timezone.now, verbose_name=_('Date-Time of'))
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

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', verbose_name=_('comment author'))
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
