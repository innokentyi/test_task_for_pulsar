from PIL import Image
from os import path

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from shop.enums import StatesChoices
from shop.helpers import split_file_to_path_and_format


class Product(models.Model):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

        ordering = ['title']

    title = models.CharField(_('title'), max_length=255)
    sku = models.CharField(_('sku'), max_length=255, unique=True)
    price = models.DecimalField(_('price'), max_digits=30, decimal_places=2, default=1000000)
    state = models.CharField(_('state'), max_length=30,  choices=StatesChoices.choices, default=StatesChoices.EXPECTED_TO_ARRIVE.value)
    slug = models.SlugField(_('slug'), max_length=255)
    category = models.ForeignKey(verbose_name=_('category'), to='Category', on_delete=models.PROTECT, related_name='products')
    image = models.ImageField(verbose_name=_('image'), upload_to=settings.MEDIA_ROOT, blank=True)

    def __str__(self):
        return self.title

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)

        # сохраним также в формате webp
        if self.image:
            img_name_without_format, img_format = split_file_to_path_and_format(self.image.name)
            if img_format != 'webp':
                image = Image.open(path.join(settings.MEDIA_ROOT, self.image.name))
                image = image.convert('RGB')
                image.save(f'{path.join(settings.MEDIA_ROOT, img_name_without_format)}.webp', 'webp')

        # todo: переделать в асинхронность или вообще поправить view обслуживающую media
        #  (если картинка в формате webp, то если нет, поискать в другом формате, конфертнуть, сохранить и вернуть ее)


class Category(models.Model):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

        ordering = ['title']

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)

    property_objects = models.ManyToManyField(verbose_name=_('properties'), to='PropertyObject')

    def __str__(self):
        return self.title


class PropertyObject(models.Model):
    class Meta:
        verbose_name = _('property object')
        verbose_name_plural = _('properties objects')

        ordering = ['title']

    class Type(models.TextChoices):
        STRING = 'string', _('string')
        DECIMAL = 'decimal', _('decimal')

    title = models.CharField(_('title'), max_length=255)
    code = models.SlugField(_('code'), max_length=255)
    value_type = models.CharField(_('value type'), max_length=10, choices=Type.choices)

    def __str__(self):
        return f'{self.title} ({self.get_value_type_display()})'


class PropertyValue(models.Model):
    class Meta:
        verbose_name = _('property value')
        verbose_name_plural = _('properties values')

        ordering = ['value_string', 'value_decimal']

    property_object = models.ForeignKey(to=PropertyObject, on_delete=models.PROTECT)

    value_string = models.CharField(_('value string'), max_length=255, blank=True, null=True)
    value_decimal = models.DecimalField(_('value decimal'), max_digits=11, decimal_places=2, blank=True, null=True)
    code = models.SlugField(_('code'), max_length=255)

    products = models.ManyToManyField(to=Product, related_name='properties')

    def __str__(self):
        return str(getattr(self, f'value_{self.property_object.value_type}', None))
