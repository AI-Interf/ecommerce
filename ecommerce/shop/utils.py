import json
from . models import *

def cookieCart(request):
	# dummy text created so there are no error on first load 
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}

	print('Cart:', cart)
	items = []
	order = {'cart_item_total': 0, 'cart_total': 0, 'delivery': False}# to make sure that the cart is empty for the unauthenticated user
	cartItems = order['cart_item_total']

	for i in cart:
		try:
			cartItems += cart[i]['quantity']

			product = Items.objects.get(id=i)
			total = (product.price * cart[i]["quantity"])

			order['cart_total'] += total
			order['cart_item_total'] += cart[i]['quantity']

			item = {
				'product':{
					'id': product.id,
					'name': product.name,
					'price': product.price,
					'imgURL': product.imgURL,
					},

				'quantity': cart[i]['quantity'],
				'item_total': total
				}

			items.append(item)

			if product.digital == False:
				order['delivery'] = True
		except:
			pass

	return {'cartItems': cartItems, 'order': order, 'items': items}

def cookieData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.cart_item_total
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']
	
	return {'cartItems': cartItems, 'order': order, 'items': items}


def guest(request, data):

	print("user not logged in")

	print('Cookies:', request.COOKIES)
	name = data['form']['name']
	email = data['form']['name']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
		email=email,
		)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for i in items:
		product = Items.objects.get(id=i['product']['id'])

		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=i['quantity']
			)

	return customer, order