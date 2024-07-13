
from django.urls import path, include
from .views import homePage, loginUser, logoutUser, customerDashboard, vendorDashboard, changePassword, search, restaurantProfile, marketPlace, restaurant,addToCart, decreaseCart,viewCart,deleteCart,checkout

urlpatterns = [
    path('', homePage, name="homePage"),
    path('login/', loginUser, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('customerDashboard/', customerDashboard, name="customerDashboard"),
    path('vendorDashboard/', vendorDashboard, name="vendorDashboard"),
    path('changePassword/', changePassword, name="changePassword"),
    path('restaurantProfile/', restaurantProfile, name="restaurantProfile"),
    path('marketPlace/', marketPlace, name="marketPlace"),
    path('restaurant/<id>', restaurant, name="restaurant"),
    path('addToCart/<id>', addToCart, name="addToCart"),
    path('decreaseCart/<id>', decreaseCart, name="decreaseCart"),
    path('viewCart', viewCart, name="viewCart"),
    path('deleteCart/<id>', deleteCart, name="deleteCart"),
    path('checkout', checkout, name="checkout"),
    path('search', search, name="search"),
]
