from django.shortcuts import render
import json
from . import models,serializers
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser,IsAuthenticated,BasePermission
from rest_framework.pagination import PageNumberPagination
import random




@api_view(['GET'])
def CategoryViewFunctionProducts(request,pk):
        productsarr=[]
        category=models.Category.objects.get(id=pk)
        products=models.Products.objects.filter(product_category=category).all()
        if products:
            for product in products:
                productsarr.append(product)
        serializer = serializers.ProductSerializer(productsarr, many=True,context={'request':request})
        return Response(serializer.data)
    
    
    
@api_view(['GET'])
def FeaturedProductView(request):
    product=models.Products.objects.filter(featured=True)
    productserializer=serializers.ProductSerializer(product,many=True,context={'request': request})        
    return Response(productserializer.data)
    
    
    
@api_view(['GET'])
def ProductDetailFunction(request,pk):  
    product=models.Products.objects.filter(id=pk)
    if product:
        productserializer=serializers.ProductSerializer(product,many=True,context={'request': request})        
    return Response(productserializer.data)


@api_view(['GET'])
def AllProductsViewFunction(request,num):
    product=list(models.Products.objects.all())
    if num!=0:
        product = random.sample(product, num)
    productserializer=serializers.ProductSerializer(product,many=True,context={'request': request})        
    return Response(productserializer.data)


@api_view(['GET'])
def AllCategoryViewFunction(request):
    category=models.Category.objects.all()
    categoryserializer=serializers.CategorySerializer(category,many=True,context={'request': request})        
    return Response(categoryserializer.data)


@api_view(['GET','POST'])
def AddProductView(request):
        product_category=json.loads(request.data['product_category'])
        print(product_category)
        # category=models.Category.objects.get(id=product_category)

        availability=True if request.data['availability']=='true' else False
        featured=True if request.data['featured']=='true' else False
        
        product_new=models.Products.objects.create(
            product_name=request.data['product_name'],
            product_picture=request.data['product_picture'],
            price=request.data['price'],
            discount=request.data['discount'],
            availability=availability,
            featured=featured,
            product_description=request.data['product_description'],
        )
        
        for i in product_category:
            category=models.Category.objects.filter(id=i)
            if category:
                product_new.product_category.add(category[0])
                product_new.save()
        
        product_new.save()
        return Response({'message':True})      