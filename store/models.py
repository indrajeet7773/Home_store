from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('Dairy', 'Dairy'),
    ('Fruits', 'Fruits'),
)

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=50, choices=[('COD', 'Cash on Delivery')])
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
