from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Fix product slug to match Google indexed URL'

    def handle(self, *args, **options):
        try:
            # Find the product (5L oil)
            product = Product.objects.get(id=11)
            
            old_slug = product.slug
            new_slug = 'karyo-mustard-oil-100-pure-cold-single-pressed-5l'
            
            # Update the slug
            product.slug = new_slug
            product.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated product slug:\n'
                    f'  Product: {product.name}\n'
                    f'  Old slug: {old_slug}\n'
                    f'  New slug: {new_slug}\n'
                    f'  URL: https://karyor.com/product/{new_slug}/'
                )
            )
        except Product.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Product not found!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
