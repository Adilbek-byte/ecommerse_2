from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder 
from .models import *

# Create your views here.
def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	# if request.user.is_authenticated:
	# 	customer = request.user.customer
	# 	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	# 	items = order.orderitem_set.all()
	# 	cartItems = order.get_cart_items
	# else:
	# 	cookieData = cookieCart(request)
	# 	cartItems = cookieData['cartItems']

		# items = []
		# order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		# cartItems = order['get_cart_items']
	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	# if request.user.is_authenticated:
	# 	customer = request.user.customer
	# 	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	# 	items = order.orderitem_set.all()
	# 	cartItems = order.get_cart_items
	# else:
	# 	cookieData = cookieCart(request)
	# 	cartItems = cookieData['cartItems']
	# 	order = cookieData['order']
	# 	items = cookieData['items']
		# try:
		# 	cart = json.loads(request.COOKIES['cart'])
		# except:
		# 	cart = {}
		# print('Cart:', cart)
		# items = []
		# order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		# cartItems = order['get_cart_items']

		# for i in cart:
		# 	try:
		# 		cartItems += cart[i]['quantity']
		# 		product = Product.objects.get(id=i)
		# 		total = (product.price * cart[i]['quantity'])
		# 		order['get_cart_total'] += total
		# 		order['get_cart_items'] += cart[i]['quantity']

		# 		item = {
		# 		'product':{
		# 		'id':product.id,
		# 		'name':product.name,
		# 		'price':product.price,
		# 		'imageUrl':product.imageUrl,
		# 		},
		# 		'quantity':cart[i]['quantity'],
		# 		'get_total':total,
		# 		}
		# 		items.append(item)

		# 		if product.digital == False:
		# 			order['shipping'] = True
		# 	except:
		# 		pass
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)



def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	# if request.user.is_authenticated:
	# 	customer = request.user.customer
	# 	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	# 	items = order.orderitem_set.all()
	# 	cartItems = order.get_cart_items
	# else:
	# 	cookieData = cookieCart(request)
	# 	cartItems = cookieData['cartItems']
	# 	order = cookieData['order']
	# 	items = cookieData['items']
		# items = []
		# order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		# cartItems = order['get_cart_items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action', action)
	print('productId', productId)
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity += 1
	elif action == 'remove':
		orderItem.quantity -= 1

	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# total = float(data['form']['total'])
		# order.transaction_id = transaction_id

		# if total == order.get_cart_total:
		# 	order.complete = True
		# order.save()

		# if order.shipping == True:
		# 	ShippingAddress.objects.create(
		# 		customer=customer,
		# 		order=order,
		# 		address=data['shipping']['address'],
		# 		city=data['shipping']['city'],
		# 		state=data['shipping']['state'],
		# 		zipcode=data['shipping']['zipcode'],
		# 		)

	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True
	order.save()
	
	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	return JsonResponse('Payment submitted...', safe=False)



