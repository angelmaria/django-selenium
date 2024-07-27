# quotes/management/commands/web_scraper.py

from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Scrapes quotes and author information from the website'
    json_file_path = 'quotes_data.json'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_mode = False

    def handle(self, *args, **options):
        self.scrape_quotes()

    def scrape_quotes(self):
        base_url = "https://quotes.toscrape.com"
        quotes = []
        authors = {}
        page = 1
        max_pages = 1 if self.test_mode else 5

        while page <= max_pages:
            url = f"{base_url}/page/{page}/"
            # Manejo de errores de red y HTTP: maneja cualquier excepción que pueda ocurrir durante la solicitud HTTP, incluyendo problemas de conexión, timeouts, y códigos de estado HTTP no exitosos.
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.RequestException as e:
                self.stdout.write(self.style.WARNING(f"Failed to fetch page {page}: {str(e)}"))
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            quote_divs = soup.find_all('div', class_='quote')

            if not quote_divs:
                break

            for quote_div in quote_divs:
                quote = {
                    'text': quote_div.find('span', class_='text').text.strip('"'),
                    'author': quote_div.find('small', class_='author').text,
                    'tags': [tag.text for tag in quote_div.find_all('a', class_='tag')]
                }
                quotes.append(quote)

                if quote['author'] not in authors:
                    author_tag = quote_div.find('a')
                    if author_tag and 'href' in author_tag.attrs:
                        author_url = base_url + author_tag['href']
                        author_info = self.scrape_author_info(author_url)
                        if author_info:
                            authors[quote['author']] = author_info
                            authors[quote['author']]['about_page_url'] = author_url 

            page += 1

        data = {
            'quotes': quotes,
            'authors': authors
        }
        # Manejo de errores al escribir el archivo JSON: maneja errores que puedan ocurrir al intentar escribir los datos scrapeados en un archivo JSON.
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.stdout.write(self.style.SUCCESS(f'Successfully scraped {len(quotes)} quotes and {len(authors)} authors'))
        except IOError as e:
            self.stdout.write(self.style.ERROR(f"Failed to write data to file: {str(e)}"))

    def scrape_author_info(self, author_url):
        # Manejo de errores al obtener información del autor: maneja errores que puedan ocurrir al intentar obtener información específica del autor.
        try:
            response = requests.get(author_url)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.WARNING(f"Failed to fetch author info from {author_url}: {str(e)}"))
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        
        born_date = soup.find('span', class_='author-born-date')
        born_location = soup.find('span', class_='author-born-location')
        about = soup.find('div', class_='author-description')

        # Manejo de elementos faltantes en la página: verifica si todos los elementos esperados están presentes en la página del autor. Si falta alguno, retorna None en lugar de intentar procesar datos incompletos.
        if not all([born_date, born_location, about]):
            return None

        born_date = born_date.text
        born_location = born_location.text
        about = about.text.strip()

        # Convert the date to YYYY-MM-DD format
        born_date = self.convert_date(born_date)

        return {
            'born': born_date,
            'birth_place': born_location.strip('in '),
            'about': about
        }

    def convert_date(self, date_str):
        # Manejo de errores de parseo de fecha: maneja el caso en que la fecha no esté en el formato esperado.
        try:
            date_obj = datetime.strptime(date_str, '%B %d, %Y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            logger.warning(f"Date '{date_str}' is not in a recognized format.")
            return None