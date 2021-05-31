from django.urls import path

from loginRegsiter.views import home, login_page,logout_page, register, product_dis

urlpatterns = [
    path('', home, name='home'),
    path('productdis/<int:id>', product_dis, name='product_dis'),
    path('loginpage/', login_page, name='loginpage'),
    path('logoutpage/', logout_page, name='logoutpage'),
    path('register/', register, name='register'),

]