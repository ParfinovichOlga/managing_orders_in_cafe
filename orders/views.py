from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views import View
from .forms import *
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from datetime import datetime

# Create your views here.


class MenuView(TemplateView):
    """Used for rendering menu page."""
    template_name = "orders/menu.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hots'] = Category.objects.get(title="HOT DRINKS").dishes.all()
        context['drinks'] = Category.objects.get(title="DRINKS").dishes.all()
        context['breakfasts'] = Category.objects.get(title="BREAKFAST").dishes.all()
        return context



class StartingPageView(View):
    """Used for rendering home page."""
    def get(self, request):
        context = {
            'form': OrderForm(),
        }
        return render(request,'orders/home.html', context)

    def post(self, request):
        """Receive table number and redirect to order page."""
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save()
            return HttpResponseRedirect(reverse('order', args=[new_order.id]))
        return render(request,'orders/home.html', {'form':form})


class MakeOrderView(View):
    """Used for rendering order page with order detail  by id."""
    def get(self, request, id):
        order = get_object_or_404(Order, id=int(id))
        ordered_dishes = order.dishes.all().order_by('title')
        menu = Menu.objects.all().order_by('title')
        context = {
            'menu':menu,
            'order':order,
            'dishes': ordered_dishes,
        }
        return render(request, 'orders/order.html', context)


class AllOrdersView(View):
    """Used for rendering page with table of all orders."""
    def get(self,request):
        orders = Order.objects.all().order_by('-order_date')
        return render(request, 'orders/all_orders.html', {'orders':orders})

    def post(self, request):
        """Filter orders by id, table_number, status"""
        form = request.POST
        orders = []
        if 'table' in form:
            if form['table'].isnumeric():
                orders = Order.objects.filter(table_number=form['table'])
                if len(orders) < 1:
                    messages.error(request,f"Table №{form['table']} has no orders")

        elif 'order_id' in form:
            if form['order_id'].isnumeric():
                orders = Order.objects.filter(id=(form['order_id']))
                if len(orders) != 1:
                    messages.error(request,f"Order {form['order_id']} doesn't exist")

        elif 'status' in form:
            orders = Order.objects.filter(status__contains=form['status'])

        return render(request, 'orders/all_orders.html', {'orders':orders})


class ReportView(View):
    """Used for rendering daily_report page."""
    def get(self, request):
        form = ReportForm()
        context = {
            'has_orders': False,
            'form':form
        }
        return render(request, 'orders/daily_report.html', context)

    def post(self,request):
        """Generate report by date."""
        form = ReportForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            orders = Order.objects.filter(Q(order_date=date), Q(status='paid'))
            has_order = False if len(orders) == 0 else True
            context = {
                'has_orders': has_order,
                'form': form,
                'orders': orders,
                'date': date,
                'day_total': get_total_price(orders)
            }
            if len(orders) == 0:
                messages.success(request,f'{date.day}-{date.month}-{date.year}: No order was paid')

            return render(request, 'orders/daily_report.html', context)
        return render(request, 'orders/daily_report.html',{'form':form, 'has_orders': False})



def update_order(order:object) -> None:
    """Update price and items in order"""
    order.price = get_total_price(order.dishes.all())
    order.items = '\n'.join([f'{dish.title} x {dish.count}' for dish in order.dishes.all()])
    order.save()


def add_dish_to_order(request, order_id:str, dish_id:str):
    """"Add dish to order if it doesn't exist or increase dish's number."""
    requested_order = get_object_or_404(Order, id=int(order_id))
    menu_item = get_object_or_404(Menu, id=int(dish_id))
    dishes = Dish.objects.filter(Q(order_id=int(order_id)),Q(title=menu_item.title))
    try:
        return HttpResponseRedirect(reverse('change', args=['increase', dishes.all()[0].id, requested_order.id]))
    except IndexError:
        ordered_dish = Dish(
            title = menu_item.title,
            price = menu_item.price,
            order_id = requested_order
        )
        ordered_dish.save()
        update_order(requested_order)
        return HttpResponseRedirect(reverse('order', args=[order_id]))


def change_number_of_dishes(request, change:str, dish_id:int, order_id:int):
    """Change dish number in order or delete dish from order."""
    upated_dish = get_object_or_404(Dish, id=dish_id)
    if change == 'reduce':
        if upated_dish.count > 1:
            upated_dish.count -= 1
            upated_dish.save()
    elif change == 'increase':
        upated_dish.count += 1
        upated_dish.save()
    elif change == 'delete':
        upated_dish.delete()
    update_order(Order.objects.get(id=order_id))
    return HttpResponseRedirect(reverse('order', args=[order_id]))


def get_total_price(dishes):
    """Count total order price or revenue per day."""
    total_price = 0
    for dish in dishes:
        try:
            total_price += dish.price * dish.count
        except AttributeError:
            total_price += dish.price
    return total_price


def change_order_status(request, order_id:int, status:str):
    """Change order status."""
    requested_order = get_object_or_404(Order, id=order_id)
    requested_order.status = status
    requested_order.save()
    return HttpResponseRedirect(reverse('order', args=[order_id]))


def delete_order(request, order_id:int):
    """Delete order by id."""
    requested_order = get_object_or_404(Order, id=order_id)
    requested_order.delete()
    return HttpResponseRedirect(reverse('all_orders'))
