from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import views from cattle app
from cattle import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
    path("whatsapp/", include("whatsapp.urls")),
    # Provide Django's built-in auth views (login/logout/password reset) at /accounts/
    path('accounts/', include('django.contrib.auth.urls')),
    # Additional accounts views (profile, orders)
    path('accounts/', include('accounts.urls')),
    path('', views.index, name='home'),
    path('health-benefits/', views.health_benefits, name='health_benefits'),
    path('products/', views.products_list, name='products_list'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/count/', views.cart_count, name='cart_count'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('payments/create-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('payments/verify-payment/', views.verify_razorpay_payment, name='verify_razorpay_payment'),
    path('payments/mark-failed/', views.mark_payment_failed, name='mark_payment_failed'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/category/<slug:slug>/', views.products_list, name='category_products'),
]

# Only add media URL in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)