from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from  .models import  *
from .utils import cookieCart
# Create your views here.
def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created  = Order.objects.get_or_create(customer = customer,complete= False )
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    products = Product.objects.all()
    context ={'products' : products ,'cartItems':cartItems}
    return render(request,'store.html',context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created  = Order.objects.get_or_create(customer = customer,complete= False )
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']


    context ={'items' : items,
              'order' :order,
              'cartItems' :cartItems
              }

    return render(request,'cart.html',context)

def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created  = Order.objects.get_or_create(customer = customer,complete= False )
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context ={'items' : items,
              'order' :order,
              'cartItems' :cartItems
              }

    return render(request,'checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print(f'ProductID : {productID}')
    print(f'Action :{action}' )

    customer = request.user.customer

    product = Product.objects.get(id =productID)

    order, created = Order.objects.get_or_create(customer = customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order = order,product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)
    
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe = False)


def processOrder(request):
    # print('Data:' , request.body)
    transaction_id = datetime.datetime.now().timestamp
    data = json.loads(request. body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True

        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode']
            )
    else:
        print('user is not logged in..')
    return JsonResponse('Payment complete!', safe = False)