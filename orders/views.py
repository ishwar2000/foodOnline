from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import orderForm
from .models import Payment, OrderedFood, Order
from accounts.context_processor import getTotal
from .utils import getOrderNumber
from home.models import userCart
# Create your views here.
@login_required(login_url='login')
def placeOrder(request):
    form = orderForm()
    cart_items = userCart.objects.filter(user=request.user)
    if request.method == "POST":
        # form = orderForm(request.POST)
        form1 = orderForm(request.POST)

        if form1.is_valid():
            amounts = getTotal(request)
            form = form1.save(commit=False)
            form.user = request.user
            form.order_number = ''
            form.total = amounts['grand_total']
            form.total_tax = 0
            form.tax_data = {}
            # print(request.POST["payment_method"])
            form.payment_method = request.POST["payment_method"]
            form.save() 
            form.order_number = getOrderNumber(form.id)
            form.save()
            # print(request.POST)
            payModel = Payment()
            payModel.user = request.user
            payModel.transaction_id = '12485' + form.order_number
            payModel.amount = amounts['grand_total']
            payModel.save()
            form.payment = payModel
            form.save()
            request.session['oid'] = form.id

            for item in cart_items:
                userOrder = OrderedFood()
                userOrder.order = form
                userOrder.payment = payModel
                userOrder.user = request.user
                userOrder.fooditem = item.foodItem
                userOrder.quantity = item.quantity
                userOrder.price = item.foodItem.price * item.quantity
                userOrder.amount = amounts['grand_total']
                userOrder.save()
            
            
                
            context = {
                "cart_items":cart_items,
                "order":form
            }

            
            return render(request, "user/placeOrder.html", context)
        else:
            print(form1.errors)
            context = {
                "cart_items":cart_items,
                "order":form
            }
            return redirect("checkout")
        
    
    return redirect("viewCart")


@login_required(login_url='login')
def orderConfirm(request):
    cart_items = userCart.objects.filter(user=request.user)
    cart_items.delete()

    oid =  request.session.get('oid')
    userOrder = Order.objects.get(id=oid)
    ordered_food = OrderedFood.objects.filter(order = userOrder)
    
    context = {
        "order":userOrder,
        "ordered_food" : ordered_food
    }
    return render(request, "user/orderConfirmation.html",context)