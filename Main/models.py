from django.db import models
from decimal import Decimal
# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=150)
    isActive=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name    
    class Meta:
        verbose_name_plural = "Category"
        db_table = "Category"


def upload_image(instance, filename):
    return "Product/{instance.product_name}/{instance.product_name}.jpg".format(instance=instance)


class Products(models.Model):
    product_name=models.CharField(max_length=150)
    product_picture=models.ImageField(upload_to=upload_image,blank=True,null=True)
    product_category=models.ManyToManyField(Category,blank=True)
    product_description=models.TextField(blank=True)
    price=models.IntegerField(default=0)
    discount=models.IntegerField(default=0)
    added_at=models.DateTimeField(auto_now_add=True)
    availability=models.BooleanField(default=False)
    featured=models.BooleanField(default=False)

    @property
    def new_price(self):
        return round((self.price-self.discount),3) 
    

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = "Product"
        db_table = "Product"