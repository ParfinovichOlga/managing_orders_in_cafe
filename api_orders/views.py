"""
Views for order APIs.
"""

from rest_framework import viewsets
from orders.models import *
from api_orders import serializers

class OrderViewSet(viewsets.ModelViewSet):
    """View for manage order APIs."""
    serializer_class = serializers.OrderDetailSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        """Retrieve orders"""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for requests."""
        if self.action == 'list':
            return serializers.OrderSerializer
        return self.serializer_class


class DishViewSet(viewsets.ModelViewSet):
    """Manage dishes."""
    serializer_class = serializers.DishSerializer
    queryset = Dish.objects.all().order_by('-id')

    def get_queryset(self):
        """Retrieve dishes"""
        return self.queryset


class CategoryViewSet(viewsets.ModelViewSet):
    """Manage categories."""
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()


class MenuViewSet(viewsets.ModelViewSet):
    """Manage menu."""
    serializer_class = serializers.MenuSerializer
    queryset = Menu.objects.all()