# quotes/management/commands/update_quotes.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
import schedule
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Runs web scraping and data import immediately and/or at regular intervals'

    def add_arguments(self, parser):
        parser.add_argument(
            '--run-once',
            action='store_true',
            help='Run the update once and exit',
        )

    def handle(self, *args, **options):
        if options['run_once']:
            self.stdout.write(self.style.SUCCESS('Running quote update once...'))
            self.run_update()
        else:
            self.stdout.write(self.style.SUCCESS('Starting quote update scheduler'))
            self.schedule_jobs()
            self.stdout.write(self.style.SUCCESS('Running initial update...'))
            self.run_update()
            self.stdout.write(self.style.SUCCESS('Initial update complete. Waiting for next scheduled run...'))
            while True:
                schedule.run_pending()
                time.sleep(1)

    def schedule_jobs(self):
        # Schedule the job to run daily at midnight
        schedule.every().day.at("00:00").do(self.run_update)

    def run_update(self):
        try:
            self.stdout.write(self.style.SUCCESS(f'Starting update at {datetime.now()}'))
            
            self.stdout.write(self.style.SUCCESS('Starting web scraping...'))
            call_command('web_scraper')
            
            self.stdout.write(self.style.SUCCESS('Web scraping completed. Starting data import...'))
            call_command('data_import')
            
            self.stdout.write(self.style.SUCCESS(f'Quote update completed successfully at {datetime.now()}'))
        except Exception as e:
            logger.error(f"An error occurred during quote update: {str(e)}")
            self.stdout.write(self.style.ERROR(f'Quote update failed: {str(e)}'))
