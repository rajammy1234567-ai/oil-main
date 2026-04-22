from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('orders/', views.orders_view, name='orders'),
    path('orders/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('orders/track/<int:pk>/', views.track_order_view, name='track_order'),
    # legacy track-order route (no pk) kept as placeholder
    path('track-order/', views.track_order_view, name='track_order_legacy'),
]
