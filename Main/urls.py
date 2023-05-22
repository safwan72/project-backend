from rest_framework import routers
from django.urls import path
from . import views
urlpatterns = [
    path("category/<int:pk>/", views.CategoryViewFunctionProducts, name="category"),
    path("addproduct/", views.AddProductView, name="addproduct"),
    path("products/<int:pk>/", views.ProductDetailFunction, name="products"),
        path("allproducts/<int:num>/", views.AllProductsViewFunction, name="allproducts"),
        path("allcategory/", views.AllCategoryViewFunction, name="allcategory"),
    path("featuredproducts/", views.FeaturedProductView, name="featuredproducts"),
]