# quotes/tests.py
import json
import os
from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, MagicMock
from quotes.management.commands.web_scraper import Command as WebScraperCommand

class WebScraperTests(TestCase):
    
    def setUp(self):
        self.test_json_path = 'test_quotes_data.json'
        self.original_json_path = WebScraperCommand.json_file_path
        WebScraperCommand.json_file_path = self.test_json_path

    def tearDown(self):
        WebScraperCommand.json_file_path = self.original_json_path
        if os.path.exists(self.test_json_path):
            os.remove(self.test_json_path)

    @patch('requests.get')
    def test_scrape_quotes_success(self, mock_get):
        html_content = '''
        <html>
            <body>
                <div class="quote">
                    <span class="text">"Life is what happens when you're busy making other plans."</span>
                    <small class="author">John Lennon</small>
                    <div class="tags">
                        <a class="tag">life</a>
                        <a class="tag">plans</a>
                    </div>
                    <a href="/author/John-Lennon">Author Page</a>
                </div>
            </body>
        </html>
        '''
        mock_response = MagicMock()
        mock_response.status_code = 200 # Simula una respuesta HTTP exitosa con contenido HTML que incluye una cita.
        mock_response.content = html_content # Verifica que el scraper extraiga correctamente la cita, el autor y las etiquetas.
        mock_get.return_value = mock_response

        cmd = WebScraperCommand()
        cmd.test_mode = True  # Activar el modo de prueba
        cmd.handle()

        self.assertTrue(os.path.exists(self.test_json_path))
        with open(self.test_json_path, 'r', encoding='utf-8') as f: ## Comprueba que los datos se guarden correctamente en un archivo JSON.
            data = json.load(f)
            self.assertEqual(len(data['quotes']), 1)
            self.assertEqual(data['quotes'][0]['text'], "Life is what happens when you're busy making other plans.")
            self.assertEqual(data['quotes'][0]['author'], "John Lennon")
            self.assertListEqual(data['quotes'][0]['tags'], ["life", "plans"])

    @patch('requests.get')
    def test_scrape_author_info_success(self, mock_get):
        html_content = '''
        <html>
            <body>
                <span class="author-born-date">October 9, 1940</span>
                <span class="author-born-location">in Liverpool, England</span>
                <div class="author-description">John Lennon was an English singer, songwriter, and peace activist.</div>
            </body>
        </html>
        '''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = html_content # Simula una respuesta HTTP exitosa con información del autor.
        mock_get.return_value = mock_response

        cmd = WebScraperCommand()
        author_info = cmd.scrape_author_info("https://quotes.toscrape.com/author/John-Lennon/") # Verifica que el scraper extraiga correctamente la fecha de nacimiento, lugar de nacimiento y biografía del autor.

        self.assertEqual(author_info['born'], '1940-10-09')
        self.assertEqual(author_info['birth_place'], 'Liverpool, England')
        self.assertEqual(author_info['about'], 'John Lennon was an English singer, songwriter, and peace activist.')

    def test_convert_date(self):
        cmd = WebScraperCommand()
        self.assertEqual(cmd.convert_date('October 9, 1940'), '1940-10-09') # Verifica que convierta correctamente una fecha en formato de texto a formato ISO.
        self.assertIsNone(cmd.convert_date('Invalid Date')) # Comprueba que devuelva None para una fecha inválida.

    @patch('requests.get')
    def test_scrape_quotes_no_quotes(self, mock_get):
        html_content = '''
        <html>
            <body>
                <div class="no-quotes"></div>
            </body>
        </html>
        '''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = html_content # Simula una respuesta HTTP sin citas.
        mock_get.return_value = mock_response

        cmd = WebScraperCommand()
        cmd.handle()

        self.assertTrue(os.path.exists(self.test_json_path))
        with open(self.test_json_path, 'r', encoding='utf-8') as f: # Verifica que el scraper maneje correctamente esta situación y guarde un archivo JSON vacío.
            data = json.load(f)
            self.assertEqual(len(data['quotes']), 0)
            
