from django.urls import path

from .views import HomeView, ProductView, BuyView, CommentView, CategoryView, SearchView

urlpatterns = [
    path('home/', HomeView.as_view()),
    path('product/<int:pk>/', ProductView.as_view()),
    path('buy/<int:pk>/', BuyView.as_view()),
    path('comment/<int:pk>/', CommentView.as_view()),
    path('home/<str:title>/', CategoryView.as_view()),
    path('search/', SearchView.as_view()),
]