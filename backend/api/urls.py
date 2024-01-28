from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('register/', views.UserRegister, name = 'register'),
    # path('user/', views.UserView.as_view(), name='user'),
    path('userAll/', views.getUserAll),
    path('profile/', views.getProfile),
    path('updateProfile/', views.updateProfile),
    path('items/', views.getItems),
    path('itemsAll/', views.getItemsAll),
    path('toSell/', views.getToSell),
    path('lost/', views.getLost),
    path('sold/', views.getSold),
    path('lostAll/', views.getLostAll),
    path('toSellAll/', views.getToSellAll),
    path('addItem/', views.addItem),
    path('addSold/', views.addSold),
    path('addLost/', views.addLost),
    path('addToSell/', views.addToSell),
    path('remToSell/', views.remToSell),
    path('remItem/', views.remItem),
    path('remLost/', views.remLost),
    path('purchased/', views.getPurchased),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
