from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
import yaml
import os
from django.db.models import Q, Sum, F
from django.db import IntegrityError
from ujson import loads as load_json


from .permissions import IsAdminUserOrOwnUser, IsShop

from .models import Shop, Category, Product, ProductInfo, CustomUser, Contact, Parameter, ProductParameter, Order, OrderItem
from .serializers import ShopSerializer, CategorySerializer, ProductSerializer, ProductInfoSerializer, \
    CustomUserSerializer, ContactSerializer, OrderSerializer, OrderItemSerializer


class CustomUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Класс для работы с пользователями
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с контактами пользователя
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        if request.user.is_staff:
            queryset = Contact.objects.all()
        else:
            queryset = Contact.objects.filter(user=user).all()
        serializer = ContactSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [IsAuthenticated()]
        elif self.action in ['destroy', 'update', 'partial_update', 'retrieve']:
            return [IsAdminUserOrOwnUser()]
        return []


class ShopViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с магазинами
    """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с категориями товаров
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с продуктами
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductInfoViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с расширенной информацией по продуктам
    """
    queryset = ProductInfo.objects.prefetch_related(
        'product_parameter__parameter')
    serializer_class = ProductInfoSerializer


class UpdatePriceViewSet(viewsets.ModelViewSet):
    """
    Класс для обновления прайса поставщика
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        file_path = os.path.join(os.getcwd(), 'data/shop1.yaml')
        with open(file_path, "r") as file:
            data = yaml.load(file.read(), Loader=yaml.Loader)
            category_relation = []
            shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
            for category in data['categories']:
                category_object, _ = Category.objects.get_or_create(name=category['name'])
                category_relation.append({'external_id': category['id'], 'internal_id': category_object.id})
            ProductInfo.objects.filter(shop_id=shop.id).delete()
            for item in data['goods']:
                for category in category_relation:
                    if item['category'] == category['external_id']:
                        internal_category = category['internal_id']
                product, _ = Product.objects.get_or_create(name=item['name'],
                                                           category_id=internal_category
                                                           )
                product_info = ProductInfo.objects.create(product_id=product.id,
                                                          shop_id=shop.id,
                                                          model=item['model'],
                                                          price=item['price'],
                                                          price_rrc=item['price_rrc'],
                                                          quantity=item['quantity'])
                for name, value in item['parameters'].items():
                    parameter_object, _ = Parameter.objects.get_or_create(name=name)
                    ProductParameter.objects.create(product_info_id=product_info.id,
                                                    parameter_id=parameter_object.id,
                                                    value=value)
        return JsonResponse({'Status': 'OK'})

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsShop()]
        elif self.action in ['destroy', 'update', 'partial_update', 'retrieve', 'list']:
            return [IsAdminUser()]
        return []


class OrderViewSet(viewsets.ModelViewSet):
    """
    Класс для работы с заказами пользователей
    """
    queryset = Order.objects.exclude(status='basket').prefetch_related('ordered_items__product_info__product__category',
                                                                       'ordered_items__product_info__product_parameter__parameter')\
        .select_related('contact').annotate(total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price')))
    serializer_class = OrderSerializer

    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        basket, _ = Order.objects.get_or_create(user_id=request.user.id, status='basket')
        items_source = request.data.get('items')
        if items_source:
            for item in items_source:
                item.update({'order': basket.id})
                serializer = OrderItemSerializer(data=item)
                print(item)
                if serializer.is_valid():
                    try:
                        serializer.save()
                    except IntegrityError as error:
                        return JsonResponse({'Status': False, 'Errors': str(error)})
                else:
                    JsonResponse({'Status': False, 'Errors': serializer.errors})

        # return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
        return JsonResponse({'Status': 'OK'})

    def list(self, request, *args, **kwargs):
       queryset = Order.objects.exclude(status='basket').prefetch_related('ordered_items__product_info__product__category',
                                                                       'ordered_items__product_info__product_parameter__parameter')\
        .select_related('contact').annotate(total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price')))
        # serializer_class = OrderSerializer
       serializer = OrderSerializer(queryset, many=True)
       return Response(serializer.data)

    # def get_permissions(self):
    #     if self.action in ['list']:
    #         return [IsAuthenticated()]
    #     elif self.action in ['destroy', 'update', 'partial_update', 'retrieve', 'list']:
    #         return [IsAdminUserOrOwnUser()]
    #     return []
