from rest_framework import serializers
from .models import CustomUser
import json
from stores.models import Store

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    stores = serializers.CharField(max_length=50,write_only=True)
    image = serializers.ImageField()
    class Meta:
        model = CustomUser
        fields = ['id','login','name','role','image','stores','password','password2']

    def validate_stores(self,value):
        stores_ids = json.loads(value)
        existing_stores_ids = Store.objects.filter(id__in = stores_ids).values_list('id',flat=True)
        if len(existing_stores_ids) < len(stores_ids):
            missing_stores_ids = set(stores_ids) - set(existing_stores_ids)
            raise serializers.ValidationError(f"Store with id {missing_stores_ids} do not exist")
        return stores_ids

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError('password and password2 must be same')
        return attrs

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        password = validated_data.pop('password')
        stores = validated_data.pop('stores')

        user = CustomUser.objects.create(
            **validated_data
        )
        user.set_password(password)
        user.save()
        user.stores.add(*stores)
        return user


class LoginSerializer(serializers.ModelSerializer):
    login = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ['id','login','password']
