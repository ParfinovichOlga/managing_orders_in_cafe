"""
URL mapping for the order app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_orders import views

router = DefaultRouter()
router.register('orders', views.OrderViewSet)
router.register('dishes', views.DishViewSet)
router.register('categories', views.CategoryViewSet)
router.register('menu', views.MenuViewSet)
app_name = 'order'

urlpatterns = [
    path('',include(router.urls))
]
