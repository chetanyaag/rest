from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('check_user', check_user, name="check_user"),
    path('check_tkn', check_tkn, name="check_user"),
    path('getProductData', getProductData, name="testing"),
    path("addAProduct", addAProduct, name="addAProduct"),
    path("get_current_deals", get_current_deals, name="get_current_deals"),
    path('create_user',create_user, name='create_user'),
    path('change_password', change_user_password, name='change_user_password'),
    path('check_admin', check_admin, name='check_admin'),
    path('get_users', get_users, name='get_users'),
    path('webhook', Webhook.as_view(), name='webhook'),
]
