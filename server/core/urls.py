from django.urls import path
from . import views

urlpatterns = [
    path('dealers/', views.dealer_list, name='dealer_list'),
    path('dealers/<int:dealer_id>/', views.dealer_detail, name='dealer_detail'),
    path('reviews/', views.review_list, name='review_list'),
    path('makes/', views.car_makes, name='car_makes'),
    path('analyze/', views.analyze_review, name='analyze_review'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/register/', views.register_view, name='register'),
]
