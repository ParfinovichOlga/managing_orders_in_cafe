from django.test import TestCase
from orders import models, views
from decimal import Decimal
from .models import *

# Create your tests here.
def create_category():
    return Category.objects.create(title='category')


def create_order(table_number=1):
    return Order.objects.create(table_number=table_number)


def create_order_with_dish():
    order = create_order()
    dish = Dish.objects.create(
        title='a',
        price = Decimal(2.5),
        count =2,
        order_id = order
    )
    dish = Dish.objects.create(
        title='b',
        price = Decimal(2.5),
        count =2,
        order_id = order
    )
    return order.dishes.all()


class TestView(TestCase):
    def test_create_category(self):
        """Test creating a category is successful."""
        category = Category.objects.create(
            title='category'
        )
        self.assertEqual(str(category), category.title)

    def test_create_menu(self):
        """Test creating a menu is successful."""
        menu = Menu.objects.create(
            title='Some menu',
            image='image',
            price=Decimal(2.5),
            category=create_category()

        )
        self.assertEqual(str(menu), f'{menu.title}: {menu.price}$')

    def test_create_order(self):
        """Test creating an order is successful."""
        order = Order.objects.create(
            table_number=8
        )
        self.assertEqual(str(order), str(order.id))

    def test_create_dish(self):
        """Test creating a dish is successful."""
        dish = Dish.objects.create(
            title='Some dish',
            price=Decimal(2.5),
            order_id=create_order()

        )
        self.assertEqual(str(dish), dish.title)


class ViewsTests(TestCase):
    def test_get_total(self):
        """Test getting correct total."""
        res = views.get_total_price(create_order_with_dish())
        self.assertEqual(res, 10)
