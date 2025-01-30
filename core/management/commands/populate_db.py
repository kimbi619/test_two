from django.core.management.base import BaseCommand
from django.conf import settings
import csv
from datetime import datetime
import logging
from core.models import Person
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates the database from the generated CSV file'

    def handle(self, *args, **options):
        try:
            filepath = os.path.join(settings.MEDIA_ROOT, 'output', 'output.csv')
            
            if not os.path.exists(filepath):
                logger.error(f"No CSV file found at {filepath}")
                return
                
            logger.info(f"Starting to process CSV file: {filepath}")
            processed_count = 0
            skipped_count = 0
            
            with open(filepath, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    try:
                        # Convert date string to datetime object
                        date_of_birth = datetime.strptime(row['DateOfBirth'], '%d/%m/%Y').date()
                        
                        # Check if record already exists
                        exists = Person.objects.filter(
                            name=row['Name'],
                            surname=row['Surname'],
                            date_of_birth=date_of_birth
                        ).exists()
                        
                        if exists:
                            skipped_count += 1
                            if skipped_count % 100 == 0:
                                logger.info(f"Skipped {skipped_count} existing records")
                            continue
                        
                        # Create new person if doesn't exist
                        Person.objects.create(
                            name=row['Name'],
                            surname=row['Surname'],
                            initials=row['Initials'],
                            age=int(row['Age']),
                            date_of_birth=date_of_birth
                        )
                        
                        processed_count += 1
                        if processed_count % 100 == 0:
                            logger.info(f"Processed {processed_count} new records")
                            
                    except Exception as e:
                        logger.error(f"Error processing row {row}: {str(e)}")
                        continue
            
            logger.info(f"Finished processing CSV file.")
            logger.info(f"New records added: {processed_count}")
            logger.info(f"Existing records skipped: {skipped_count}")
            
        except Exception as e:
            logger.error(f"Error processing CSV file: {str(e)}")
            raise 