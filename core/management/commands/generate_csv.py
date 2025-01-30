from django.core.management.base import BaseCommand
from django.conf import settings
import csv
import os
import random
from datetime import datetime
import logging
from core.models import Person
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample data arrays
NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", 
    "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", 
    "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"
]

SURNAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", 
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
]

class Command(BaseCommand):
    help = 'Generates a CSV file with random person data'

    def add_arguments(self, parser):
        parser.add_argument('records_count', type=int, help='Number of records to generate')

    def handle(self, *args, **options):
        try:
            records_count = options['records_count']
            logger.info(f"Starting to generate {records_count} records")
            
            output_dir = os.path.join(settings.MEDIA_ROOT, 'output')
            os.makedirs(output_dir, exist_ok=True)
            logger.info(f"Output directory created/verified: {output_dir}")
            
            filename = os.path.join(output_dir, 'output.csv')
            logger.info(f"Will write to file: {filename}")
            
            headers = ['Id', 'Name', 'Surname', 'Initials', 'Age', 'DateOfBirth']
            generated_records = set()
            fake = Faker()
            
            initial_count = Person.objects.count()
            if initial_count > 0:
                logger.info(f"Clearing {initial_count} existing records from database")
                Person.objects.all().delete()
            
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                logger.info("CSV headers written")
                
                for i in range(records_count):
                    attempts = 0
                    while True:
                        attempts += 1
                        name = random.choice(NAMES)
                        surname = random.choice(SURNAMES)
                        dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
                        age = (datetime.now().date() - dob).days // 365
                        initials = name[0]
                        
                        record = (name, surname, dob)
                        if record not in generated_records:
                            generated_records.add(record)
                            
                            row_data = [i + 1, name, surname, initials, age, dob.strftime('%d/%m/%Y')]
                            writer.writerow(row_data)
                            
                            try:
                                Person.objects.create(
                                    name=name,
                                    surname=surname,
                                    initials=initials,
                                    age=age,
                                    date_of_birth=dob
                                )
                                
                                if (i + 1) % 100 == 0:
                                    logger.info(f"Progress: {i + 1}/{records_count} records created")
                                    logger.info(f"Last record: {name} {surname}, Age: {age}")
                                
                                break
                                
                            except Exception as db_error:
                                logger.error(f"Database error on record {i + 1}: {str(db_error)}")
                                raise
                        
                        if attempts > 100:
                            logger.warning(f"Many attempts needed to generate unique record at position {i + 1}")
            
            # Final statistics
            final_count = Person.objects.count()
            logger.info(f"Task completed successfully!")
            logger.info(f"CSV file created at: {filename}")
            logger.info(f"Total records in database: {final_count}")
            logger.info(f"Total unique combinations generated: {len(generated_records)}")
            
        except Exception as e:
            logger.error(f"Fatal error in generate_csv: {str(e)}")
            logger.exception("Full traceback:")
            raise
