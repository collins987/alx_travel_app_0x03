from django.core.management.base import BaseCommand
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

        def handle(self, *args, **kwargs):
                sample_listings = [
                            {
                                            'title': 'Beach House',
                                                            'description': 'A beautiful house by the beach.',
                                                                            'price_per_night': 150.00,
                                                                                            'location': 'Mombasa',
                                                                                                            'available': True
                                                                                                                        },
                                                                                                                                    {
                                                                                                                                                    'title': 'Mountain Cabin',
                                                                                                                                                                    'description': 'A cozy cabin in the mountains.',
                                                                                                                                                                                    'price_per_night': 200.00,
                                                                                                                                                                                                    'location': 'Mt. Kenya',
                                                                                                                                                                                                                    'available': True
                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                            {
                                                                                                                                                                                                                                                            'title': 'City Apartment',
                                                                                                                                                                                                                                                                            'description': 'Modern apartment in the city center.',
                                                                                                                                                                                                                                                                                            'price_per_night': 100.00,
                                                                                                                                                                                                                                                                                                            'location': 'Nairobi',
                                                                                                                                                                                                                                                                                                                            'available': True
                                                                                                                                                                                                                                                                                                                                        },
                                                                                                                                                                                                                                                                                                                                                ]

                                                                                                                                                                                                                                                                                                                                                        for data in sample_listings:
                                                                                                                                                                                                                                                                                                                                                                    Listing.objects.get_or_create(**data)

                                                                                                                                                                                                                                                                                                                                                                            self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
                                                                                                                                                                                                                                                                                                                                                                            