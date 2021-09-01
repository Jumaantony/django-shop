from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
    # list of all products
    path('', views.product_list, name='product_list'),

    # list of products in a given category
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),

    # product detail
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]