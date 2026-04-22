from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms2 import UserForm, ProfileForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


@login_required
def profile_view(request):
    user = request.user
    try:
        profile = user.profile
    except Exception:
        profile = None

    if request.method == 'POST':
        uf = UserForm(request.POST, instance=user)
        pf = ProfileForm(request.POST, instance=profile)
        if uf.is_valid() and pf.is_valid():
            # Save user and profile
            uf.save()
            pf.save()

            # Handle optional password fields (from the form)
            pwd = request.POST.get('password')
            pwdc = request.POST.get('password_confirm')
            if pwd or pwdc:
                if pwd != pwdc:
                    messages.error(request, 'Passwords do not match.')
                    return render(request, 'registration/profile.html', {'user_form': uf, 'profile_form': pf})
                if len(pwd) < 8:
                    messages.error(request, 'Password must be at least 8 characters long.')
                    return render(request, 'registration/profile.html', {'user_form': uf, 'profile_form': pf})
                # set password and keep the user logged in
                user.set_password(pwd)
                # ensure username is synced with email so login by email works
                if uf.cleaned_data.get('email'):
                    user.username = uf.cleaned_data.get('email')
                user.save()
                update_session_auth_hash(request, user)

            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        uf = UserForm(instance=user)
        pf = ProfileForm(instance=profile)

    # If redirected from checkout with missing fields, expose them as a list for the template
    missing_qs = request.GET.get('missing') if request and hasattr(request, 'GET') else None
    missing_list = []
    if missing_qs:
        try:
            missing_list = [m for m in missing_qs.split(',') if m]
        except Exception:
            missing_list = []

    return render(request, 'registration/profile.html', {'user_form': uf, 'profile_form': pf, 'missing_list': missing_list})


@login_required
def orders_view(request):
    # Query orders belonging to the logged-in user
    try:
        from orders.models import Order
        # Exclude orders that are only created but not completed (e.g., user abandoned payment)
        orders = Order.objects.filter(user=request.user).exclude(status='created').order_by('-created_at')
    except Exception:
        orders = []
    # Enrich orders with a preview title/image so templates don't have to guess JSON shape
    try:
        from products.models import Product
    except Exception:
        Product = None

    for o in orders:
        preview_title = f"Order #{o.pk}"
        preview_image = ''
        if o.items:
            for k, v in (o.items.items() if isinstance(o.items, dict) else []):
                # If stored as a dict with product data
                if isinstance(v, dict):
                    title = v.get('title') or v.get('name')
                    img = v.get('image')
                    if title:
                        preview_title = title
                        preview_image = img or ''
                        break
                else:
                    # v is likely a quantity; try to lookup product by key
                    try:
                        if Product is not None:
                            prod = Product.objects.filter(pk=int(k)).first()
                            if prod:
                                preview_title = prod.name
                                preview_image = prod.main_image or ''
                                break
                    except Exception:
                        continue
        # attach attributes for template usage
        setattr(o, 'preview_title', preview_title)
        setattr(o, 'preview_image', preview_image)

    return render(request, 'accounts/orders.html', {'orders': orders})


@login_required
def track_order_view(request, pk=None):
    # If pk provided, show detailed tracking for that order; otherwise render a generic tracking page
    if pk:
        from orders.models import Order
        order = get_object_or_404(Order, pk=pk, user=request.user)
        # Build a clear timeline of status steps. We don't have per-step timestamps,
        # so use created_at for 'Order placed', use updated_at as a fallback for intermediate steps,
        # and delivery_date for estimated delivery when available.
        status_flow = [
            ('created', 'Order placed', 'Your order has been placed.'),
            ('processing', 'Processing', 'Your order is being processed.'),
            ('confirmed', 'Confirmed', 'Your order has been confirmed.'),
            ('paid', 'Payment processed', 'Your payment has been received.'),
            ('shipped', 'Shipped', 'Your item has been shipped.'),
            ('out_for_delivery', 'Out for delivery', 'Your item is out for delivery.'),
            ('delivered', 'Delivered', 'Your item has been delivered.'),
            ('failed', 'Payment failed', 'Payment failed or order could not be completed.'),
        ]

        # determine which step is current so we can mark completed steps
        current_index = -1
        for idx, (c, _, _) in enumerate(status_flow):
            if c == order.status:
                current_index = idx
                break

        timeline = []
        for idx, (code, title, desc) in enumerate(status_flow):
            step = {'code': code, 'title': title, 'desc': desc, 'time': None, 'is_current': False, 'is_completed': False}
            if code == 'created':
                step['time'] = order.created_at
            elif code == 'paid' and order.razorpay_payment_id:
                step['time'] = order.updated_at
            elif code == 'delivered' and order.status == 'delivered':
                step['time'] = order.updated_at
            elif code == 'failed' and order.status == 'failed':
                step['time'] = order.updated_at
            elif code == 'out_for_delivery' and order.status == 'out_for_delivery':
                step['time'] = order.updated_at
            elif code == 'shipped' and order.status == 'shipped':
                step['time'] = order.updated_at
            # mark the current and completed steps
            if idx == current_index:
                step['is_current'] = True
            if current_index >= 0 and idx <= current_index:
                step['is_completed'] = True
            timeline.append(step)

        # Add estimated delivery as a separate informative step if present
        if order.delivery_date:
            timeline.append({'code': 'eta', 'title': 'Estimated delivery', 'desc': f'Estimated delivery date: {order.delivery_date}', 'time': order.delivery_date, 'is_current': False})

        return render(request, 'accounts/track_order.html', {'order': order, 'timeline': timeline})
    return render(request, 'accounts/track_order.html')


@login_required
def order_detail_view(request, pk):
    from orders.models import Order
    order = get_object_or_404(Order, pk=pk, user=request.user)
    # Do not show orders that are still in 'created' state (abandoned/cancelled before payment)
    if getattr(order, 'status', None) == 'created':
        return redirect('accounts:orders')
    # determine payment method
    payment_method = 'Online Payment' if order.razorpay_payment_id else 'Cash On Delivery'
    # address from profile if available
    addr = None
    try:
        addr = request.user.profile
    except Exception:
        addr = None
    # Normalize items into a list of dicts for the template to consume safely
    items_list = []
    try:
        from products.models import Product
    except Exception:
        Product = None

    if order.items and isinstance(order.items, dict):
        for k, v in order.items.items():
            item = {'title': str(k), 'image': '', 'price': order.amount, 'quantity': 1, 'options': ''}
            if isinstance(v, dict):
                item['title'] = v.get('title') or v.get('name') or item['title']
                item['image'] = v.get('image') or ''
                item['price'] = v.get('price') or item['price']
                item['quantity'] = v.get('quantity') or item['quantity']
                # prefer variant then options keys
                item['options'] = v.get('variant') or v.get('options') or ''
            else:
                # v is a primitive (likely quantity) — try to resolve product
                try:
                    if Product is not None:
                        prod = Product.objects.filter(pk=int(k)).first()
                        if prod:
                            item['title'] = prod.name
                            item['image'] = prod.main_image or ''
                            item['price'] = prod.price or item['price']
                except Exception:
                    pass
                try:
                    item['quantity'] = int(v)
                except Exception:
                    item['quantity'] = 1
            items_list.append(item)

    return render(request, 'accounts/order_detail.html', {'order': order, 'payment_method': payment_method, 'address': addr, 'items': items_list})
