from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cookieData, guest
from .models import *
# Create your views here.

# method for shop
def shop(request):
	data = cookieData(request)
	cartItems = data['cartItems']
	
	item = Items.objects.all()

	context = {
		'item': item,
		'cartItems': cartItems,
	}

	return render(request, 'shop/shop.html', context)



# method for cart
def cart(request):
	data = cookieData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
		'items': items,
		'order': order,
		'cartItems': cartItems,
	}

	return render(request, 'shop/cart.html', context)



# method for checkout
def checkout(request):
	data = cookieData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
		'items': items,
		'order': order,
		'cartItems': cartItems,
	}

	return render(request, 'shop/checkout.html', context)




def updateItem(request):
	data = json.loads(request.body)#setting the value to the response and passing the data
	itemID = data['itemID']# getting the itemId that we set in js file
	action = data['action']# getting the action that we set in js file

	print('Action:', action)
	print('itemID:', itemID)

	customer = request.user.customer #getting the logged in customer
	item = Items.objects.get(id=itemID)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=item)

	# if we add the item than order item gets increase by one and vise-versa
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	# if the order item is equal or less than zero than the item gets deleted 
	if orderItem.quantity <= 0:
		orderItem.delete()
	
	return JsonResponse("Item was added", safe=False)




def process(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guest(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total ==float(order.cart_total):
		order.complete = True
	order.save()

	if order.delivery == True:
		Delivery.objects.create(
			customer=customer,
			order=order,
			address=data['delivery']['address'],
			city=data['delivery']['city'],
			state=data['delivery']['state'],				
		)

	return JsonResponse("Pyament completed", safe=False)
