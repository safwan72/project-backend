from django.dispatch.dispatcher import receiver
from django.shortcuts import render
from . import models, serializers
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer
    
    
class AuthSerializerView(generics.CreateAPIView, generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    

    
@api_view(['GET'])
def AllCustomersView(request):
    users=models.User.objects.filter(is_superuser=False,is_staff=False)
    userSerializer=serializers.UserSerializer(users,many=True,context={'request': request})        
    return Response(userSerializer.data)
