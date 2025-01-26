from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from orders.models import *
from api_orders.serializers import *
import random
from decimal import Decimal
from datetime import datetime
from django.urls import reverse
# Create your tests here.

ORDER_URL = reverse('order:order-list')
DISH_URL = reverse('order:dish-list')

def detail_url(order_id):
    """Create and return a order detail URL."""
    return reverse('order:order-detail', args=[order_id])


def create_order(**params):
    """Create and return a sample order."""
    defaults = {
        'table_number': random.randint(1,10),
        'order_date': datetime.now(),
        'price': Decimal(2.5),
        'status': 'processed',
        'items': 'A few items'
    }
    defaults.update(params)
    order = Order.objects.create(**defaults)
    return order


class OrderAPITests(TestCase):
    """Test API requests."""
    def test_order_request(self):
        """Test retrieving a list of orders."""
        create_order()
        create_order()
        self.client = APIClient()
        res = self.client.get(ORDER_URL)
        orders = Order.objects.all().order_by('-id')
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_order_detail(self):
        """Test get order detail"""
        order = create_order()
        url = detail_url(order.id)
        res = self.client.get(url)

        serializer = OrderDetailSerializer(order)
        self.assertEqual(res.data, serializer.data)


class DishAPITtests(TestCase):
    """Test API requests."""
    def set_up(self):
        self.client = APIClient()

    def test_retrieve_dishes(self):
        order = create_order()
        Dish.objects.create(order_id=order, title='Coffee', price=Decimal(2.5))
        Dish.objects.create(order_id=order, title='Tea', price=Decimal(1.5))

        res = self.client.get(DISH_URL)

        dishes = Dish.objects.all().order_by('-id')
        serializer = DishSerializer(dishes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
