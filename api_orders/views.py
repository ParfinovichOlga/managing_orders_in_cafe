"""
Views for order APIs.
"""

from rest_framework import viewsets
from orders.models import *
from api_orders import serializers
from drf_spectacular.utils import(
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

ORDER_STATUS = ['processed', 'ready', 'paid']


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

@extend_schema_view(
    list = extend_schema(
        parameters=[
            OpenApiParameter(
                'table_number',
                OpenApiTypes.STR
            ),
            OpenApiParameter(
                'id',
                OpenApiTypes.STR
            ),
            OpenApiParameter(
                'status',
                OpenApiTypes.STR, enum = ORDER_STATUS
            ),
        ]
    )
)
class OrderViewSet(viewsets.ModelViewSet):
    """Manage order."""
    serializer_class = serializers.OrderDetailSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        table_number = self.request.query_params.get('table_number')
        id = self.request.query_params.get('id')
        status = self.request.query_params.get('status')
        queryset = self.queryset
        if table_number:
            queryset = queryset.filter(table_number=table_number)
        if id:
            queryset = queryset.filter(id=id)
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-id')


    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.OrderSerializer
        return self.serializer_class
