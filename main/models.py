from django.db import models
from account.models import User


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Review(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    review = models.TextField()


#order
class Order(models.Model):
    ORDER_STATUS = (
        ('Paid', 'paid'),
        ('Not Paid', 'notpaid')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    discount = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(choices=ORDER_STATUS, max_length=30, default='notpaid')
    delivery_address = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.status} {self.user}'


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_products', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity


