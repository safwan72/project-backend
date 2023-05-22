from django.db import models
from App_Login.models import User
from Main.models import Products
from decimal import Decimal

# Create your models here.

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orderer')
    product=models.ForeignKey(Products,on_delete=models.CASCADE,blank=True)
    quantity=models.IntegerField(default=1)
    purchased=models.BooleanField(default=False)
    added_time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.product.product_name} X {self.quantity}'
    @property
    def product_total(self):
        price=(self.product.new_price*self.quantity)
                
        return round(price,3)
    class Meta:
        ordering=['-added_time',]
        verbose_name_plural='Cart'
    
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    shipping_address = models.TextField(blank=True, null=True)
    delivery_charge=models.IntegerField(default=50)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.user.username}\'s X  Order'
    @property
    def total_price(self):
        total=0
        for i in self.items.all():
           total+=float(i.product_total)
        total=total+self.delivery_charge
        return total 
    @property
    def total_price_after_discount(self):
        total=0
        for i in self.items.all():
           total+=float(i.product_total)
        total=total+self.delivery_charge
        if self.coupon is not None:
            total=total-self.coupon.amount
        return total 

   