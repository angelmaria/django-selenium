# quotes/management/commands/data_import.py

import json
from django.core.management.base import BaseCommand
from quotes.models import Author, Quote, Tag, QuoteTag

class Command(BaseCommand):
    help = 'Imports quotes and authors data from JSON file'

    def handle(self, *args, **options):
        with open('quotes_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Import authors
        for author_name, author_info in data['authors'].items():
            author, created = Author.objects.get_or_create(
                name=author_name,
                defaults={
                    'about': author_info.get('about', ''),
                    'born': author_info.get('born', None),
                    'birth_place': author_info.get('birth_place', ''),
                    'about_page_url': author_info.get('about_page_url', '')  # Correct handling of the URL
                }
            )

        # Import quotes and tags
        for quote_data in data['quotes']:
            author = Author.objects.get(name=quote_data['author'])
            quote, created = Quote.objects.get_or_create(
                text=quote_data['text'],
                author=author
            )

            for tag_name in quote_data['tags']:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                QuoteTag.objects.get_or_create(quote=quote, tag=tag)
        
        self.stdout.write(self.style.SUCCESS('Successfully imported data'))
