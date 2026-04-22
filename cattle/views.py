import os
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone


def index(request):
    # Try to load active banners from the website app; fall back to demo data when DB/migrations aren't ready
    banners = []
    mini_slides = []
    hero_bg = ''
    try:
        from website.models import Banner

        qs_hero = Banner.objects.filter(is_active=True, slot=Banner.SLOT_HERO).order_by('order', '-created_at')
        qs_mini = Banner.objects.filter(is_active=True, slot=Banner.SLOT_MINI).order_by('order', '-created_at')

        for b in qs_hero:
            banners.append({
                'id': b.pk,
                'title_en': b.title or '',
                'title_hi': b.title or '',
                'description_en': b.alt_text or '',
                'description_hi': b.alt_text or '',
                'image_url': b.image.url if b.image else '',
                'link_url': b.link or '#'
            })

        for m in qs_mini:
            mini_slides.append({
                'id': m.pk,
                'image_url': m.image.url if m.image else '',
                'alt_text': m.alt_text or ''
            })

        hero_bg = banners[0]['image_url'] if banners and banners[0].get('image_url') else ''

        # If no banners found in DB, trigger fallback to use demo data
        if not banners:
            raise Exception("No banners found")
    except Exception:
        # Database not ready or website app not migrated; use demo banners
        banners = [
            {
                'id': 1,
                'title_en': 'Karyor Premium Mustard Oil',
                'title_hi': 'कार्योर प्रीमियम सरसों का तेल',
                'description_en': 'Premium quality 100% pure mustard oil for authentic taste',
                'description_hi': 'असली स्वाद के लिए प्रीमियम गुणवत्ता वाला 100% शुद्ध सरसों का तेल',
                'image_url': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&q=80&w=1920',
                'link_url': '/products/mustard-oil/'
            },
            {
                'id': 2,
                'title_en': 'Health & Purity',
                'title_hi': 'स्वास्थ्य और शुद्धता',
                'description_en': 'Made from carefully selected mustard seeds',
                'description_hi': 'सावधानीपूर्वक चुनी गई सरसों से बना',
                'image_url': 'https://images.unsplash.com/photo-1615485925763-867862f80c29?auto=format&fit=crop&q=80&w=1920',
                'link_url': '/products/mustard-oil/'
            }
        ]
        mini_slides = [
            {'id': 1, 'image_url': 'https://images.unsplash.com/photo-1547005327-ef31e9c56cae?auto=format&fit=crop&q=80&w=600', 'alt_text': 'Mini 1'},
            {'id': 2, 'image_url': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?auto=format&fit=crop&q=80&w=600', 'alt_text': 'Mini 2'},
        ]
        hero_bg = banners[0]['image_url'] if banners and banners[0].get('image_url') else ''
    # Load categories and featured products from products app when available
    categories_list = []
    featured_products = []
    try:
        from products.models import Category, Product

        for c in Category.objects.all():
            categories_list.append({
                'id': c.pk,
                'name_en': c.name,
                'name_hi': c.name,
                'slug': c.slug,
                'icon': 'fas fa-box',
                'image_url': c.image.url if c.image else '',
                'product_count': c.products.filter(is_active=True).count()
            })

        qs = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')[:8]
        for p in qs:
            featured_products.append({
                'id': p.pk,
                'name_en': p.name,
                'name_hi': p.name,
                'description_en': p.short_description or '',
                'description_hi': p.short_description or '',
                'price': float(p.price),
                'discount_percentage': float(p.discount_percentage or 0),
                'final_price': float(p.price) * (1 - float(p.discount_percentage or 0) / 100),
                'image_url': p.main_image or '/static/images/product1.jpg',
                'category': p.category.name if p.category else '',
                'slug': p.slug,
                'in_stock': True,
                'variants': []
            })
    except Exception:
        # fallback demo lists
        categories_list = [
            {
                'id': 1,
                'name_en': 'Mustard Oil',
                'name_hi': 'सरसों का तेल',
                'slug': 'mustard-oil',
                'icon': 'fas fa-bottle-droplet',
                'image_url': '',
                'product_count': 15
            },
            {
                'id': 2,
                'name_en': 'Spices',
                'name_hi': 'मसाले',
                'slug': 'spices',
                'icon': 'fas fa-pepper-hot',
                'image_url': '',
                'product_count': 25
            },
            {
                'id': 3,
                'name_en': 'Pickles',
                'name_hi': 'अचार',
                'slug': 'pickles',
                'icon': 'fas fa-jar',
                'image_url': '',
                'product_count': 12
            },
            {
                'id': 4,
                'name_en': 'Grains',
                'name_hi': 'अनाज',
                'slug': 'grains',
                'icon': 'fas fa-wheat',
                'image_url': '',
                'product_count': 8
            },
        ]
        featured_products = [
            {
                'id': 1,
                'name_en': 'Karyor Premium Mustard Oil (1L)',
                'name_hi': 'कार्योर प्रीमियम सरसों का तेल (1L)',
                'description_en': '100% Pure Kachi Ghani Mustard Oil',
                'description_hi': '100% शुद्ध कच्ची घानी सरसों का तेल',
                'price': 185,
                'discount_percentage': 10,
                'final_price': 166.5,
                'image_url': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&q=80&w=800',
                'category': 'Mustard Oil',
                'slug': 'premium-mustard-oil-1l',
                'in_stock': True,
                'variants': [
                    {'weight': '1L', 'price': 185},
                    {'weight': '5L', 'price': 850}
                ]
            },
            {
                'id': 2,
                'name_en': 'Karyor Premium Mustard Oil (5L)',
                'name_hi': 'कार्योर प्रीमियम सरसों का तेल (5L)',
                'description_en': 'Family Pack - 100% Pure',
                'description_hi': 'फैमिली पैक - 100% शुद्ध',
                'price': 900,
                'discount_percentage': 5,
                'final_price': 855.0,
                'image_url': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&q=80&w=800',
                'category': 'Mustard Oil',
                'slug': 'premium-mustard-oil-5l',
                'in_stock': True,
                'variants': [
                    {'weight': '5L', 'price': 900}
                ]
            },
        ]

    context = {
        'banners': banners,
        'mini_slides': mini_slides,
        'hero_bg': hero_bg,
        'categories': categories_list,
        'featured_products': featured_products,
        'videos': [],
        'feed_types': []
    }

    try:
        from website.models import FeedType
        context['feed_types'] = list(FeedType.objects.filter(is_active=True).order_by('order'))
    except Exception:
        pass
    # Attempt to load videos from the videos app (admin-uploaded). Fall back to demo data when DB isn't ready.
    try:
        from videos.models import Video

        videos_list = []
        qs_v = Video.objects.filter(is_active=True).order_by('order', '-created_at')[:12]
        for v in qs_v:
            # Determine type based on the explicit source field
            if v.source == Video.SOURCE_FILE:
                vtype = 'file'
                vurl = v.video_file.url if v.video_file else ''
                youtube_watch = ''
                youtube_id = ''
            else:
                vtype = 'embed'
                # Normalize common YouTube URLs to embed format so we always play via iframe
                raw = (v.embed_url or '').strip()
                vurl = raw
                youtube_watch = ''
                youtube_id = ''
                try:
                    import re
                    if raw:
                        # If already embed URL, keep as-is and try to extract id
                        if 'youtube.com/embed' in raw:
                            m = re.search(r'/embed/([A-Za-z0-9_-]{11})', raw)
                            if m:
                                youtube_id = m.group(1)
                                vurl = raw
                        else:
                            # try to extract video id from watch?v= or youtu.be links
                            m = re.search(r'(?:v=|v/|youtu\.be/|embed/)([A-Za-z0-9_-]{11})', raw)
                            if m:
                                youtube_id = m.group(1)
                                vurl = f'https://www.youtube.com/embed/{youtube_id}'
                    # also prepare a watch URL for fallbacks
                    if youtube_id:
                        youtube_watch = f'https://www.youtube.com/watch?v={youtube_id}'
                except Exception:
                    # if anything goes wrong, fall back to the raw embed_url
                    vurl = raw
                    youtube_watch = raw

            # Derive thumbnail for YouTube if not provided
            if v.thumbnail:
                thumb = v.thumbnail.url
            else:
                if vtype == 'embed' and youtube_id:
                    # Use YouTube's generated thumbnail
                    thumb = f'https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg'
                elif vtype == 'file' and v.video_file:
                    # No image thumbnail for uploaded files: fallback to a generic image
                    thumb = '/static/images/video1.jpg'
                else:
                    thumb = '/static/images/video1.jpg'

            videos_list.append({
                'id': v.pk,
                'title_en': v.title,
                'title_hi': v.title,
                'youtube_url': vurl,
                'thumbnail_url': thumb,
                'video_type': vtype,
                'watch_url': youtube_watch,
                'youtube_id': youtube_id,
            })
        context['videos'] = videos_list
    except Exception:
        # leave demo videos if import fails or DB not ready
        context['videos'] = [
            {
                'id': 1,
                'title_en': 'Benefits of Mustard Oil',
                'title_hi': 'सरसों के तेल के फायदे',
                'description_en': 'Learn about the health benefits of pure mustard oil',
                'description_hi': 'शुद्ध सरसों के तेल के स्वास्थ्य लाभों के बारे में जानें',
                'youtube_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                'thumbnail_url': '/static/images/video1.jpg',
                'video_type': 'embed',
            },
            {
                'id': 2,
                'title_en': 'Karyor Manufacturing Process',
                'title_hi': 'कार्योर निर्माण प्रक्रिया',
                'description_en': 'See how we maintain 100% purity',
                'description_hi': 'देखें कि हम 100% शुद्धता कैसे बनाए रखते हैं',
                'youtube_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                'thumbnail_url': '/static/images/video2.jpg',
                'video_type': 'embed',
            }
        ]
    return render(request, 'home/index.html', context)


def health_benefits(request):
    """Render the health benefits page for cold & single pressed mustard oil."""
    return render(request, 'health_benefits.html')


def products_list(request, slug=None):
    # Use Product models when available; otherwise fall back to demo data
    products = []
    try:
        from products.models import Product, Category
        from django.db.models import Q

        qs = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'tags')
        # search query
        q = request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(short_description__icontains=q) | Q(tags__name__icontains=q)
            ).distinct()
        if slug:
            try:
                cat = Category.objects.get(slug=slug)
                qs = qs.filter(category=cat)
            except Category.DoesNotExist:
                qs = Product.objects.none()

        for p in qs:
            products.append({
                'id': p.pk,
                'name': p.name,
                'short_description': p.short_description,
                'price': float(p.price),
                'discount_percentage': float(p.discount_percentage or 0),
                'final_price': float(p.price) * (1 - float(p.discount_percentage or 0) / 100),
                'image_url': p.main_image or '/static/images/product1.jpg',
                'slug': p.slug,
                'in_stock': True,
                'category': p.category.name if p.category else ''
            })
    except Exception:
        # demo product data if DB isn't ready
        products = [
            {
                'id': 1,
                'name': 'Karyor Premium Mustard Oil',
                'short_description': '100% Pure Kachi Ghani Mustard Oil',
                'price': 185,
                'discount_percentage': 10,
                'final_price': 166.5,
                'image_url': '/static/images/product1.jpg',
                'slug': 'premium-mustard-oil',
                'in_stock': True,
                'category': 'Mustard Oil'
            }
        ]
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, slug):
    try:
        from products.models import Product
        p = Product.objects.prefetch_related('images').select_related('category').get(slug=slug, is_active=True)
        image_gallery = [img.image.url for img in p.images.all()]
        # normalize availability to the values templates expect
        avail = getattr(p, 'availability', '')
        if avail == 'available':
            availability = 'in_stock'
        elif avail == 'out_of_stock':
            availability = 'out_of_stock'
        else:
            availability = avail or ''
        product = {
            'id': p.pk,
            'name': p.name,
            'short_description': p.short_description,
            'long_description': p.long_description,
            'price': float(p.price),
            'discount_percentage': float(p.discount_percentage or 0),
            'final_price': float(p.price) * (1 - float(p.discount_percentage or 0) / 100),
            'image_url': p.main_image or (image_gallery[0] if image_gallery else '/static/images/product1.jpg'),
            'image_gallery': image_gallery,
            'category': {'name': p.category.name if p.category else '', 'slug': p.category.slug if p.category else ''},
            'how_to_use': p.how_to_use,
            'details': p.details or {},
            'additional_details': p.additional_details or '',
            
            'availability': availability,
            'social': {
                'facebook': p.social_facebook,
                'instagram': p.social_instagram,
                'x': p.social_x,
                'youtube': p.social_youtube,
            },
            'offers': [
                {
                    'title': o.title,
                    'description': o.description,
                    # use discount_value from Offer (if present) for display
                    'discount_percentage': float(getattr(o, 'discount_percentage', getattr(o, 'discount_value', 0) or 0))
                } for o in p.offers.filter(active=True)
            ],
            'tags': [t.name for t in p.tags.all()]
        }
    except Exception:
        # fallback demo product
        product = {
            'id': 1,
            'name': 'Karyor Premium Mustard Oil',
            'long_description': 'Premium quality 100% pure mustard oil made from carefully selected mustard seeds for authentic taste, aroma, and health benefits.',
            'price': 185,
            'discount_percentage': 10,
            'final_price': 166.5,
            'image_url': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&q=80&w=800',
            'image_gallery': ['https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&q=80&w=800', 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&q=80&w=800'],
            'category': {'name': 'Mustard Oil', 'slug': 'mustard-oil'},
            'how_to_use': 'Use for cooking',
            'details': {}
        }
    return render(request, 'products/product_detail.html', {'product': product})


def add_to_cart(request):
    # Accept POST with product_id and quantity; store in session cart
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        import json
        data = json.loads(request.body.decode('utf-8'))
        product_id = str(data.get('product_id'))
        quantity = int(data.get('quantity', 1))
    except Exception:
        return JsonResponse({'error': 'invalid payload'}, status=400)

    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    request.session['cart'] = cart
    total_items = sum(cart.values())
    return JsonResponse({'success': True, 'cart_count': total_items})


def cart_view(request):
    # Render cart page showing products in session cart
    cart = request.session.get('cart', {})
    items = []
    total = 0.0
    if cart:
        try:
            from products.models import Product
            ids = [int(pid) for pid in cart.keys()]
            qs = Product.objects.filter(pk__in=ids)
            prod_map = {p.pk: p for p in qs}
            for pid_str, qty in cart.items():
                pid = int(pid_str)
                p = prod_map.get(pid)
                if not p:
                    continue
                price = float(p.price)
                line = price * int(qty)
                total += line
                items.append({
                    'id': p.pk,
                    'name': p.name,
                    'price': price,
                    'quantity': int(qty),
                    'image_url': p.main_image or 'https://images.unsplash.com/photo-1547005327-ef31e9c56cae?auto=format&fit=crop&q=80&w=200',
                    'line_total': line,
                    'slug': p.slug,
                })
        except Exception:
            items = []
    context = {'items': items, 'total': total}
    # expose razorpay key so base.html can include checkout script when available
    context['razorpay_key'] = getattr(settings, 'RAZORPAY_KEY_ID', '')
    return render(request, 'cart/cart.html', context)


def update_cart(request):
    # Accept POST JSON {product_id, quantity} to set quantity or remove
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        import json
        data = json.loads(request.body.decode('utf-8'))
        product_id = str(data.get('product_id'))
        quantity = int(data.get('quantity', 0))
    except Exception:
        return JsonResponse({'error': 'invalid payload'}, status=400)

    cart = request.session.get('cart', {})
    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = quantity
    request.session['cart'] = cart

    # Recalculate totals
    total = 0.0
    count = 0
    try:
        from products.models import Product
        ids = [int(pid) for pid in cart.keys()]
        qs = Product.objects.filter(pk__in=ids)
        prod_map = {p.pk: p for p in qs}
        for pid_str, qty in cart.items():
            pid = int(pid_str)
            p = prod_map.get(pid)
            if not p:
                continue
            total += float(p.price) * int(qty)
            count += int(qty)
    except Exception:
        total = sum([0])
        count = sum(cart.values()) if cart else 0

    return JsonResponse({'success': True, 'cart_count': count, 'cart_total': total})


def cart_count(request):
    """Return current cart item count from session as JSON."""
    cart = request.session.get('cart', {})
    count = sum(int(q) for q in cart.values()) if cart else 0
    return JsonResponse({'cart_count': count})


def create_razorpay_order(request):
    """Create a Razorpay order for the given amount (expects POST JSON {amount: <rupees>, receipt: <optional>}).
    Returns the created order and the public key for client-side checkout.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        import json
        data = json.loads(request.body.decode('utf-8'))
        amount = data.get('amount')
        receipt = data.get('receipt', None)
        if amount is None:
            return JsonResponse({'error': 'amount required'}, status=400)
        # amount expected in rupees (float/int) — convert to paise
        amount_paise = int(round(float(amount) * 100))

        # If user is authenticated, ensure profile has required contact details
        try:
            if request.user and request.user.is_authenticated:
                profile = getattr(request.user, 'profile', None)
                missing = []
                if not profile or not getattr(profile, 'phone', None):
                    missing.append('phone')
                if not profile or not getattr(profile, 'address_line1', None):
                    missing.append('address')
                if missing:
                    qs = 'missing=' + ','.join(missing)
                    return JsonResponse({'success': False, 'profile_required': True, 'missing': missing, 'redirect': f'/accounts/profile/?{qs}'}, status=400)
        except Exception:
            # if anything unexpected happens, allow checkout to proceed (do not block)
            pass

        # Lazy import razorpay (may not be installed in all environments)
        try:
            import razorpay
        except Exception:
            return JsonResponse({'error': 'razorpay client not available. Run `pip install razorpay`'}, status=500)

        key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
        key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
        if not key_id or not key_secret:
            return JsonResponse({'error': 'razorpay keys not configured. Please set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in your environment.'}, status=500)

        client = razorpay.Client(auth=(key_id, key_secret))
        # ensure a unique receipt/order reference for each created order
        local_receipt = receipt or f"ORD-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        order_data = {
            'amount': amount_paise,
            'currency': 'INR',
            'payment_capture': 1,
            'receipt': str(local_receipt)
        }

        try:
            order = client.order.create(data=order_data)
        except Exception as ex:
            # Provide clearer guidance when auth fails
            msg = str(ex)
            if 'Authentication' in msg or 'auth' in msg.lower():
                return JsonResponse({'error': 'failed to create order', 'details': 'Authentication failed - check RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET'}, status=500)
            return JsonResponse({'error': 'failed to create order', 'details': msg}, status=500)

        # Persist an Order record (best-effort; if orders app not migrated this will fail silently)
        try:
            from orders.models import Order
            cart_items = request.session.get('cart', {})
            # persist order with our generated receipt (or razorpay's) so we have a stable uid
            Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                razorpay_order_id=order.get('id'),
                amount=float(amount),
                currency=order.get('currency', 'INR'),
                status='created',
                receipt=str(local_receipt),
                items=cart_items
            )
        except Exception:
            # ignore persistence errors here to avoid blocking checkout
            pass

        return JsonResponse({'success': True, 'order': order, 'key': key_id})
    except Exception as e:
        return JsonResponse({'error': 'failed to create order', 'details': str(e)}, status=500)


def verify_razorpay_payment(request):
    """Verify Razorpay payment signature (expects POST JSON with razorpay_payment_id, razorpay_order_id, razorpay_signature).
    Returns success True if signature is valid.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        import json
        data = json.loads(request.body.decode('utf-8'))
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')
        if not (payment_id and order_id and signature):
            return JsonResponse({'error': 'missing parameters'}, status=400)

        try:
            import razorpay
        except Exception:
            return JsonResponse({'error': 'razorpay client not available. Run `pip install razorpay`'}, status=500)

        key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
        key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
        if not key_id or not key_secret:
            return JsonResponse({'error': 'razorpay keys not configured. Please set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in your environment.'}, status=500)

        client = razorpay.Client(auth=(key_id, key_secret))
        params = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        try:
            client.utility.verify_payment_signature(params)
            # Signature valid — update Order record if present
            try:
                from orders.models import Order
                o = Order.objects.filter(razorpay_order_id=order_id).first()
                if o:
                    o.razorpay_payment_id = payment_id
                    o.razorpay_signature = signature
                    o.status = 'paid'
                    # clear session cart after successful payment
                    try:
                        request.session.pop('cart', None)
                        request.session.modified = True
                    except Exception:
                        pass
                    o.save()
            except Exception:
                pass
            return JsonResponse({'success': True})
        except Exception as ex:
            # mark order as failed if we can
            try:
                from orders.models import Order
                o = Order.objects.filter(razorpay_order_id=order_id).first()
                if o:
                    o.status = 'failed'
                    o.save()
            except Exception:
                pass
            msg = str(ex)
            if 'Authentication' in msg or 'auth' in msg.lower():
                return JsonResponse({'success': False, 'error': 'signature_verification_failed', 'details': 'Authentication failed - check Razorpay keys'}, status=400)
            return JsonResponse({'success': False, 'error': 'signature_verification_failed', 'details': msg}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'invalid payload', 'details': str(e)}, status=400)


def mark_payment_failed(request):
    """Mark order as failed when payment fails (expects POST JSON {razorpay_order_id})."""
    if request.method != 'POST':
        return JsonResponse({'success': False})
    try:
        import json
        data = json.loads(request.body.decode('utf-8'))
        order_id = data.get('razorpay_order_id')
        if not order_id:
            return JsonResponse({'success': False})
        from orders.models import Order
        order = Order.objects.filter(razorpay_order_id=order_id).first()
        if order:
            order.status = 'failed'
            order.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})