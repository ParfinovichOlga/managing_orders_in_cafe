from django.urls import path
from .import views

urlpatterns = [
    path('', views.StartingPageView.as_view(), name='home'),
    path('order/<id>', views.MakeOrderView.as_view(), name='order'),
    path('add_dish_to_order/<order_id>/<dish_id>', views.add_dish_to_order, name='add_dish'),
    path('change/<change>/<dish_id>/<order_id>', views.change_number_of_dishes, name='change'),
    path('all_orders', views.AllOrdersView.as_view(), name='all_orders'),
    path('cange_order_status/<order_id>/<status>', views.change_order_status, name='change_status'),
    path('delete_order/<order_id>', views.delete_order, name='delete_order'),
    path('report', views.ReportView.as_view(), name='report'),
    path('menu', views.MenuView.as_view(), name='menu')


]