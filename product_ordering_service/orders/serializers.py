from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

from .models import Shop, Category, Product, ProductInfo, ProductParameter, CustomUser, Contact


# Формирование токена при регистрации пользователя
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'company', 'position')
        read_only_fields = ('id',)

    def validate(self, data):
        fields_validate = ['first_name', 'last_name', 'company', 'position']
        for field in fields_validate:
            if data.get(field) is None:
                raise ValidationError(f'the {field} field is not filled in')
        return data

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ContactSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Contact
        extra_kwargs = {'user': {'write_only': True}}
        fields = ('id', 'user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone')
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ShopSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Shop
        extra_kwargs = {'user': {'write_only': True}}
        fields = ('id', 'name', 'url', 'user', 'is_active')
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'category')
        read_only_fields = ('id',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value',)


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_parameter = ProductParameterSerializer(read_only=True, many=True)
    shop = serializers.StringRelatedField()

    class Meta:
        model = ProductInfo
        fields = ('id', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameter')
        read_only_fields = ('id',)
