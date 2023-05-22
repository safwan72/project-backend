from django.views.decorators.csrf import requires_csrf_token
from rest_framework import serializers
from . import models
from App_Login.serializers import UserSerializer
from Main.serializers import ProductSerializer
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupon
        fields = "__all__"
        depth=1
        
        


class MyCartSerializer(serializers.ModelSerializer):
    user=UserSerializer(required=False)
    product_total=serializers.SerializerMethodField()
    product_total_discount=serializers.SerializerMethodField()
    class Meta:
        model = models.Cart
        fields = "__all__"
        depth=1
        
    def get_product_total(self, obj):
        return round((obj.product.new_price))
    def get_product_total_discount(self, obj):
        return round((obj.product.new_price*obj.quantity))
    
    
class MyOrderSerializer(serializers.ModelSerializer):
    user=UserSerializer(required=False)
    items=MyCartSerializer(many=True,required=False)
    total_price=serializers.SerializerMethodField()
    total_price_after_discount=serializers.SerializerMethodField()
    coupon=CouponSerializer(required=False)
    class Meta:
        model = models.Order
        fields = "__all__"
        depth=1
    def get_total_price(self, obj):
        return obj.total_price
    def get_total_price_after_discount(self, obj):
        return obj.total_price_after_discount

