from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=100, null=True)
	email = models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.name

class Items(models.Model):
	name = models.CharField(max_length=100, null=True)
	price = models.FloatField()
	digital = models.BooleanField(default=False, null=True, blank=False)
	img = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	# property decorator which makes sure there is no error if there are no img uploaded
	@property
	def imgURL(self):
		try:
			url = self.img.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	order_date= models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def delivery(self):
		delivery = False
		order = self.orderitem_set.all()
		for i in order:
			if i.product.digital == False:
				delivery = True
		return delivery
	

	# decorator to get the sum of all the cart items
	@property
	def cart_total(self):
		order = self.orderitem_set.all()#query all child orderitems
		total = sum([item.item_total for item in order])#ran loop and calculate the item total value
		return total

	# decorator to find the total items in the cart
	@property
	def cart_item_total(self):
		order = self.orderitem_set.all()#query all child orderitems
		total_items = sum([item.quantity for item in order])#ran loop and calculate the total items in the cart
		return total_items
	

class OrderItem(models.Model):
	product = models.ForeignKey(Items, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	added_date = models.DateTimeField(auto_now_add=True)

	# decorator to get he sum of all the items
	@property
	def item_total(self):
		total = self.product.price * self.quantity
		return total
	

class Delivery(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	order= models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	address = models.CharField(max_length=100, null=True)
	city = models.CharField(max_length=100, null=True)
	state = models.CharField(max_length=100, null=True)
	added_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address