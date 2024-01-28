from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from .models import User, Profile, Items, Lost, Purchased, toSell, Sold

class UserSerializer( serializers.ModelSerializer ):
    class Meta:
        model= User
        fields = ('id', 'email', 'role')

class ProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

class LostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lost
        fields = '__all__'

class PurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchased
        fields = '__all__'

class toSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = toSell
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def create(self, clean_data):
        user = User.objects.create_superuser(**clean_data)
        return user

class SoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sold
        fields = '__all__'