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

ORDER_URL = reverse('ord:order-list')
DISH_URL = reverse('ord:dish-list')

def detail_url(order_id):
    """Create and return a order detail URL."""
    return reverse('ord:order-detail', args=[order_id])


def create_order(**params):
    """Create and return a sample order."""
    defaults = {
        'table_number': random.randint(1,10),
        'price': Decimal(2.5),
        'status': 'processed',
        'items': 'A few items'
    }
    defaults.update(params)
    order = Order.objects.create(**defaults)
    return order


class OrderAPITests(TestCase):
    """Test API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_order_request(self):
        """Test retrieving a list of orders."""
        create_order()
        create_order()
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

    def test_create_dish_on_update(self):
        """Test creating dish when update an order."""
        order = create_order()
        payload = {'dishes': [{'title': 'new_dish', 'price': Decimal('2.5')}]}
        url = detail_url(order.id)

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_dish = Dish.objects.get(order_id=order.id, title='new_dish')
        self.assertIn(new_dish, order.dishes.all())

    def test_update_order_assign_dish(self):
        """Test assigning an existing tag when updating a recipe."""
        coffee = Dish.objects.create(title='Coffee', price=Decimal(2.5))
        order = create_order()
        order.dishes.add(coffee)

        payload = {'dishes': [{'title': 'Soup', 'price': Decimal('4.0')}]}
        url = detail_url(order.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(coffee, order.dishes.all())
        self.assertEqual(order.dishes.count(), 1)
        self.assertEqual('Soup', order.dishes.all()[0].title)


    def test_clear_order_dishes(self):
        """Test clearing an order dishes."""
        dish = Dish.objects.create(title='Coffee', price=Decimal('2'))
        order = create_order()
        order.dishes.add(dish)

        payload = {'dishes': []}
        url = detail_url(order.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(order.dishes.count(), 0)

    def test_filter_by_table(self):
        """Test filtering orders by table number."""
        ord1 = create_order(table_number=1)
        create_order(table_number=1)
        ord3 = create_order(table_number=2)

        params = {'table_id': {ord1.table_number}}
        res = self.client.get(ORDER_URL, params)
        orders = Order.objects.filter(table_number=ord1.table_number)

        self.assertIn(OrderSerializer(ord1).data,
                         res.data)
        self.assertNotIn(OrderSerializer(ord3), res.data)
        self.assertEqual(orders.count(), 2)

    def test_filter_by_order_id(self):
        """Test filtering orders by order id."""
        create_order()
        create_order()
        ord = create_order()

        params = {'id': {ord.id}}
        res = self.client.get(ORDER_URL, params)
        s = OrderSerializer(ord, many=False)

        self.assertEqual(res.data[0], s.data)

    def test_filter_by_order_status(self):
        """Test filtering orders by status."""
        paid_order = create_order(status='paid')
        create_order(status='paid')
        proceed_order = create_order()

        params = {'status': 'paid'}
        res = self.client.get(ORDER_URL, params)
        paid = Order.objects.filter(status='paid')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertIn(OrderSerializer(paid_order).data, res.data)
        self.assertNotIn(OrderSerializer(proceed_order).data, res.data)


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
