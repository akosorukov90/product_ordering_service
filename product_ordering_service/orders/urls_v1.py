from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .api_views_v1 import ShopViewSet, CategoryViewSet, ProductViewSet, ProductInfoViewSet, CustomUserViewSet,\
    ContactViewSet, UpdatePriceViewSet

from rest_framework.authtoken import views

router = DefaultRouter()
router.register('shop', ShopViewSet, basename='shops')
router.register('category', CategoryViewSet, basename='categorys')
router.register('product', ProductViewSet, basename='products')
router.register('product_info', ProductInfoViewSet, basename='product_infos')
router.register('register', CustomUserViewSet, basename='register_user')
router.register('contacts', ContactViewSet, basename='contacts_user')
router.register('update_price', UpdatePriceViewSet, basename='update_prices')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
