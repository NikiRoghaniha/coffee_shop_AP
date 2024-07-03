from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Storage(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    amount = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    image = models.ImageField(null=True)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)
    ingredients = models.ManyToManyField('Storage', through='Ingredient')

    def __str__(self):
        return self.name

    def has_enough_stock(self):
        for ingredient in Ingredient.objects.filter(product=self):
            if ingredient.storage.amount < ingredient.quantity:
                return False
        return True

    def reduce_stock(self):
        for ingredient in Ingredient.objects.filter(product=self):
            ingredient.storage.amount -= ingredient.quantity
            ingredient.storage.save()


class Ingredient(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    is_takeaway = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, )
    amount = models.PositiveIntegerField(default=0)

    def update_amount(self):
        self.amount = sum(item.product.price * item.quantity for item in OrderItem.objects.filter(order=self))
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.reduce_stock()
        self.order.update_amount()


class HomePageSlider(models.Model):
    sort = models.IntegerField(unique=True)
    image = models.ImageField()
    active = models.BooleanField(default=False)
