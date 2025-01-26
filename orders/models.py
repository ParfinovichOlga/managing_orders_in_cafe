"""
Database models
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

ORDER_STATUS = (('processed', 'processed'), ('ready', 'ready'), ('paid', 'paid'))
MIN_TABLE_NUMBER = 1
MAX_TABLE_NUMBER = 10
# Create your models here.


class Category(models.Model):
    """Category object."""
    title = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Categories'


class Menu(models.Model):
    """Menu object."""
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images')
    price = models.DecimalField(max_digits=3, decimal_places=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes', null=True)

    def __str__(self):
        return f'{self.title}: {self.price}$'

    class Meta:
        verbose_name_plural = 'Menu'


class Order(models.Model):
    """Order object."""
    table_number = models.IntegerField(validators=[MinValueValidator(MIN_TABLE_NUMBER),\
                                                     MaxValueValidator(MAX_TABLE_NUMBER)])
    order_date = models.DateField(auto_now=True)
    price = models.DecimalField(max_digits=1000000000, decimal_places=1, default=0)
    status = models.CharField(choices=ORDER_STATUS, default='processed', max_length=25)
    items = models.CharField(max_length=5000, blank=True)

    def __str__(self):
        return f'{self.id}'


class Dish(models.Model):
    """Dish object."""
    title = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=3, decimal_places=1)
    count = models.IntegerField(default=1)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='dishes', null=True)

    class Meta:
        verbose_name_plural = 'Dishes'

    def __str__(self):
        return f'{self.title}'


