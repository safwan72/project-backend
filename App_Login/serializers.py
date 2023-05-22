from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from json import dumps

class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("id","username", "phone","date_joined","password")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def create(self, validated_data):
        user = models.User.objects._create_user(
            phone=validated_data['phone'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
    
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['phone'] = user.phone
        # token['date_joined']=dumps(user.date_joined)
        token['isAdmin']=user.is_staff
        return token