from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path('', views.category_list, name="category"),
    path('product_list/', views.product_list, name='product_list'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.user_login, name='user_login'),
    # path('logout/', views.user_logout, name='user_logout'),
    path('my_profile/', views.my_profile, name='user_profile'),


    path("categories/", views.category_list, name="category_list"),
    path("categories/new/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),

    path("products/", views.product_list, name="product_list"),
    path("products/new/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
]
