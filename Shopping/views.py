from App_Login.models import User
from django.shortcuts import render
from . import models,serializers
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Main.models import Products
from django.shortcuts import render, get_object_or_404
import json
from App_Login.models import User
    
    
class CartModelView(viewsets.ModelViewSet):
    queryset=models.Cart.objects.all()
    serializer_class=serializers.MyCartSerializer
    
    
    def create(self,request):
        user=request.data['user'] 
        user=User.objects.get(id=user)  
        product=request.data['product']
        products=Products.objects.filter(id=product)
        product=products[0]
        cart=models.Cart.objects.get_or_create(
            user=user,
            product=product,
            purchased=False
        )
        order=models.Order.objects.filter(
            user=user,
            ordered=False,
        )
        if order.exists():
            order=order[0]
            if order.items.filter(product=product).exists():
                cart[0].quantity += 1
                cart[0].save()
                order.save()
            else:
                order.cart_items.add(cart[0])
                order.save()
        else:
            order=models.Order.objects.create(
                user=user,
            ordered=False
            )
            order.cart_items.add(cart[0])
            order.save()    
        return Response({'message':'Product Added To Cart'})
    
@api_view(['GET','POST'])
def increase_product(request,pk):
    product = get_object_or_404(Products, pk=pk)
    user=get_object_or_404(User,id=request.data['id'])  
    cart=models.Cart.objects.get_or_create(product=product,user=user,purchased=False)
    order=models.Order.objects.filter(user=user,ordered=False)
    if order.exists():
        order=order[0]
        if order.items.filter(product=product).exists():
            cart[0].quantity+=1
            cart[0].save()
            order.save()
        else:
            order.items.add(cart[0])
            order.save()
    else:
        order=models.Order.objects.create(user=user,ordered=False)
        order.save()
        order.items.add(cart[0])
        order.save()
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request}) 
    return Response({'order':orderserializer.data})


@api_view(['GET','POST'])
def decrease_product(request,pk):
    product = get_object_or_404(Products, pk=pk)
    user=get_object_or_404(User,id=request.data['id'])
    order=models.Order.objects.filter(user=user,ordered=False)
    if order.exists():
        order=order[0]
        if order.items.filter(product=product).exists():
            cart=models.Cart.objects.filter(product=product,user=user,purchased=False)
            cart=cart[0]
            if cart.quantity>1:
                    cart.quantity-=1
                    cart.save()
            else:
                    order.items.remove(cart)
                    cart.delete()
                    cart.save()
                    order.save()      
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request}) 
    return Response({'order':orderserializer.data})



@api_view(['PUT','GET'])
def add_coupon(request,pk):
    user=get_object_or_404(User,id=pk)  
    order=models.Order.objects.filter(user=user,ordered=False)
    mycoupon=request.data['coupon']
    coupon=models.Coupon.objects.filter(code=mycoupon)
    if coupon.exists():
        coupon=coupon[0]
        if order.exists():
            order=order[0]
            order.coupon=coupon
            order.save()
        return Response({'coupon':True})        
    else:
        return Response({'coupon':'Check Your Coupon. It is invalid '})
       
# @api_view(['PUT','GET'])
# def add_address(request,pk):
#     user=get_object_or_404(User,id=pk,roles='Customer')  
#     customer = get_object_or_404(Customer, user=user)
#     order=models.Order.objects.filter(user=customer,ordered=False)
#     myaddress=request.data['address']    
#     if order.exists():
#         order=order[0]
#         order.shipping_address=myaddress
#         order.save()
#         return Response({'status':True})        
#     else:
#         return Response({'status':False})        
    
@api_view(['GET','POST'])
def my_cart(request,pk):
    user=get_object_or_404(User,id=pk)
    print(user)  
    order=models.Order.objects.filter(user=user,ordered=False)
    if order.exists():
        order=order[0]
        orderserializer=serializers.MyOrderSerializer(order,context={'request': request})
        return Response({'order':orderserializer.data})
    else:
        return Response({'order':False})


    
@api_view(['GET','POST'])
def my_recent_orders(request,pk):
    user=get_object_or_404(User,id=pk)  
    order=models.Order.objects.filter(user=user,ordered=True)
    if order.exists():
        orderserializer=serializers.MyOrderSerializer(order,context={'request': request},many=True)
        return Response({'order':orderserializer.data})
    else:
        return Response({'order':False})

    
@api_view(['GET','POST'])
def all_orders(request):
    order=models.Order.objects.all().exclude(ordered=False)
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request},many=True)
    return Response(orderserializer.data)


    
@api_view(['GET','POST'])
def order_by_id(request,pk):
    order=models.Order.objects.filter(id=pk)
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request},many=True)
    return Response(orderserializer.data)
    
    
@api_view(['GET','POST'])
def checkout(request,pk):
    user=get_object_or_404(User,id=pk)
    order=models.Order.objects.filter(user=user,ordered=False)
    if order.exists():
        order=order[0]
        order.shipping_address=request.data['address']
        cart=models.Cart.objects.filter(user=user,purchased=False)
        if cart:
            cart=cart[0]
        order.ordered=True
        cart.purchased=True
        cart.save()
        order.save()
    return Response({'status':'ok'})



