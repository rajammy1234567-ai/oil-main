from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Update product names, slugs, and descriptions for better SEO'

    def handle(self, *args, **options):
        updates = []
        
        try:
            # Update 1L Product
            product_1l = Product.objects.get(id=10)
            old_name_1l = product_1l.name
            old_slug_1l = product_1l.slug
            
            product_1l.name = 'KARYOR 100% Pure Cold & Single Pressed Mustard Oil (1L)'
            product_1l.slug = 'karyor-mustard-oil-100-pure-cold-single-pressed-1l'
            product_1l.short_description = 'Premium quality 100% pure cold & single pressed mustard oil - 1 Liter pack. Perfect for authentic Indian cooking with rich aroma and natural flavor.'
            product_1l.save()
            
            updates.append({
                'id': 10,
                'old_name': old_name_1l,
                'new_name': product_1l.name,
                'old_slug': old_slug_1l,
                'new_slug': product_1l.slug,
                'url': f'https://karyor.com/product/{product_1l.slug}/'
            })
            
        except Product.DoesNotExist:
            self.stdout.write(self.style.WARNING('1L Product (ID: 10) not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating 1L product: {str(e)}'))
        
        try:
            # Update 5L Product
            product_5l = Product.objects.get(id=11)
            old_name_5l = product_5l.name
            old_slug_5l = product_5l.slug
            
            product_5l.name = 'KARYOR 100% Pure Cold & Single Pressed Mustard Oil (5L)'
            # Keep the existing slug that we just fixed
            product_5l.short_description = 'Premium quality 100% pure cold & single pressed mustard oil - 5 Liter family pack. Ideal for traditional cooking with authentic taste and health benefits.'
            product_5l.save()
            
            updates.append({
                'id': 11,
                'old_name': old_name_5l,
                'new_name': product_5l.name,
                'old_slug': old_slug_5l,
                'new_slug': product_5l.slug,
                'url': f'https://karyor.com/product/{product_5l.slug}/'
            })
            
        except Product.DoesNotExist:
            self.stdout.write(self.style.WARNING('5L Product (ID: 11) not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating 5L product: {str(e)}'))
        
        # Display results
        if updates:
            self.stdout.write(self.style.SUCCESS('\n✓ Successfully updated products:\n'))
            for update in updates:
                self.stdout.write(f"\n{'='*60}")
                self.stdout.write(f"Product ID: {update['id']}")
                self.stdout.write(f"Old Name: {update['old_name']}")
                self.stdout.write(f"New Name: {update['new_name']}")
                self.stdout.write(f"Old Slug: {update['old_slug']}")
                self.stdout.write(f"New Slug: {update['new_slug']}")
                self.stdout.write(self.style.SUCCESS(f"URL: {update['url']}"))
                self.stdout.write(f"{'='*60}\n")
            
            self.stdout.write(self.style.SUCCESS('\n✓ All products updated successfully!'))
            self.stdout.write(self.style.WARNING('\nNext steps:'))
            self.stdout.write('1. Visit your website to verify the changes')
            self.stdout.write('2. Update Google Search Console (if configured)')
            self.stdout.write('3. Request re-indexing for better Google search results')
        else:
            self.stdout.write(self.style.WARNING('No products were updated'))
