# Person Management System

A Django-based system for managing person records with CSV import/export capabilities.

## Project Overview

This Django application provides functionality to:
- Manage person records (name, surname, initials, age, date of birth)
- Generate random person data and export to CSV
- Import person data from CSV files
- View person records through a web interface

## Project Structure 

## Setup

1. Clone the repository
2. Create a virtual environment:

## Models

### Person Model
Located in `core/models.py`, the Person model includes:
- `name` (CharField): Person's first name
- `surname` (CharField): Person's last name
- `initials` (CharField): Person's initials
- `age` (IntegerField): Person's age (0-120)
- `date_of_birth` (DateField): Person's birth date

The model includes a unique constraint on the combination of name, surname, and date of birth.

## Management Commands

### Generate CSV Command
Generate random person data and export to CSV:
```bash
python manage.py generate_csv <number_of_records>
```
This command:
- Generates specified number of random person records
- Exports data to `media/output/output.csv`
- Clears existing database records
- Populates database with new records

### Populate Database Command
Import data from CSV to database:
```bash
python manage.py populate_db
```
This command:
- Reads from `media/output/output.csv`
- Skips existing records (based on name, surname, and date of birth)
- Creates new person records in the database

## Views

### PersonListView
- URL: `/`
- Displays a list of all persons in the database
- Template: `core/person_list.html`

## Media Files

The project uses a media directory for storing generated CSV files:
- Media root: `media/`
- CSV output directory: `media/output/`
- CSV file path: `media/output/output.csv`

## Development Settings

The project includes development settings in `test_two/settings.py`:
- SQLite database
- Debug mode enabled
- Media files configured
- Static files configured

## Important Notes

1. The current setup is for development only and is a test submission for the test two project.

2. The CSV generation includes a uniqueness check to avoid duplicate records

3. Both management commands include logging for monitoring progress and debugging

## Error Handling

The application includes comprehensive error handling:
- CSV generation and database population errors are logged
- Duplicate records are handled gracefully
- File system errors are caught and reported

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

