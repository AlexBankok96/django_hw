from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json

class Command(BaseCommand):
    help = 'Populate the database with categories and products from fixtures'

    @staticmethod
    def json_read_categories():
        with open('fixtures/catalog_data.json') as f:
            data = json.load(f)
            return [item for item in data if item['model'] == 'catalog.category']

    @staticmethod
    def json_read_products():
        with open('fixtures/catalog_data.json') as f:
            data = json.load(f)
            return [item for item in data if item['model'] == 'catalog.product']

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()


        product_for_create = []
        category_for_create = []


        for category in Command.json_read_categories():
            category_for_create.append(
                Category(name=category['fields']['name'],
                         description=category['fields'].get('description', ''))
            )
        Category.objects.bulk_create(category_for_create)


        for product in Command.json_read_products():
            category = Category.objects.get(pk=product['fields']['category'])
            product_for_create.append(
                Product(name=product['fields']['name'],
                        description=product['fields'].get('description', ''),
                        category=category,
                        price=product['fields']['price'])
            )
        Product.objects.bulk_create(product_for_create)
