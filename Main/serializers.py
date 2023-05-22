from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Category
        fields='__all__'
        depth=1
        
        
class ProductSerializer(serializers.ModelSerializer):
    product_category=CategorySerializer(many=True,required=False)
    product_picture=serializers.SerializerMethodField()
    new_price=serializers.SerializerMethodField()
    class Meta:
        model=models.Products
        fields='__all__'
        depth=1
    def get_new_price(self, obj):
        return obj.new_price

    def get_product_picture(self, obj):
        request = self.context.get('request')
        product_picture = obj.product_picture.url
        return request.build_absolute_uri(product_picture)
    
    
    