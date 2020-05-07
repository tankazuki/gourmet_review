from django.urls import path
from . import views


app_name = "techapp"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search', views.search, name='search'),
    path('shop_info/<str:restid>', views.shopinfo, name='shopinfo'),
    path('signup/', views.Signup.as_view(), name='signup'),
]
