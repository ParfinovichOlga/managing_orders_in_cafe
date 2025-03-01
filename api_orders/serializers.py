"""
Serializers for order APIs
"""

from rest_framework import serializers
from orders.models import Order, Dish, Category, Menu


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories in menu."""
    class Meta:
        model = Category
        fields = ['id', 'title']
        read_only_fields = ['id']


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for menu."""
    class Meta:
        model = Menu
        fields = ['id', 'title', 'image', 'price', 'category']
        read_only_fields = ['id']


class DishSerializer(serializers.ModelSerializer):
    """Serializer for dishes."""
    class Meta:
        model = Dish
        fields = ['id', 'title', 'price', 'count', 'order_id']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders."""
    class Meta:
        model = Order
        fields = ['id', 'table_number', 'order_date', 'price', 'status', 'items']
        read_only_fields = ['id']


class OrderDetailSerializer(OrderSerializer):
    """Serializer for order detail view."""
    dishes = DishSerializer(many=True, required=False)
    class Meta(OrderSerializer.Meta):
        fields = OrderSerializer.Meta.fields + ['dishes']

    def _get_or_create_dish(self, dishes, order):
        """Handle getting or creating dishes as needed."""
        for dish in dishes:
            dish_obj = Dish.objects.create(
                order_id = order,
                **dish
            )
            order.dishes.add(dish_obj)

    def update(self, instance, validated_data):
        """Update order."""
        dishes = validated_data.pop('dishes', None)
        if dishes is not None:
            instance.dishes.clear()
            self._get_or_create_dish(dishes, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
