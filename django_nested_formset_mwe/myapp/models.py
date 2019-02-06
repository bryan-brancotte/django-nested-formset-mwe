from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Promotion(models.Model):
    year = models.IntegerField(
        verbose_name=_('year_label'),
        help_text=_('year_help_text'),
    )
    name = models.CharField(
        verbose_name=_('name_label'),
        help_text=_('name_help_text'),
        max_length=64,
    )

    def __str__(self):
        return "Promotion %i (%s)" % (self.year, self.name)

    def get_absolute_url(self):
        return reverse('myapp:promotion-detail', kwargs={'pk': self.pk})


class Student(models.Model):
    promotion = models.ForeignKey(
        to=Promotion,
        verbose_name=_('promotion_label'),
        help_text=_('promotion_help_text'),
        on_delete=models.CASCADE,
        related_name='students',
    )
    first_name = models.CharField(
        verbose_name=_('first_name_label'),
        help_text=_('first_name_help_text'),
        max_length=64,
    )
    last_name = models.CharField(
        verbose_name=_('last_name_label'),
        help_text=_('last_name_help_text'),
        max_length=64,
    )

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Address(models.Model):
    student = models.ForeignKey(
        to=Student,
        verbose_name=_('first_name_label'),
        help_text=_('first_name_help_text'),
        on_delete=models.CASCADE,
        related_name='addresses',
    )
    full_address = models.CharField(
        verbose_name=_('full_address_label'),
        help_text=_('full_address_help_text'),
        max_length=256,
    )
    main_address = models.BooleanField(
        verbose_name=_('main_address_label'),
        help_text=_('main_address_help_text'),
        default=False,
    )

    def __str__(self):
        return  self.full_address
