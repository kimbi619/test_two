from flask import Flask, render_template, request, send_file
import os
import csv
import random
import sqlite3
from datetime import datetime, timedelta
import string
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'


for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
    if not os.path.exists(folder):
        os.makedirs(folder)


NAMES = [
    "Sean", "Sasha", "John", "Emma", "Michael", 
    "Sarah", "David", "Lisa", "James", "Anna",
    "Robert", "Maria", "William", "Elizabeth", "Richard",
    "Jennifer", "Thomas", "Jessica", "Daniel", "Emily"
]


SURNAMES = [
    "Pompeii", "Hall", "Smith", "Johnson", "Williams",
    "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore"
]


def create_database():
    """Create SQLite database and table"""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS csv_import
                 (Id INTEGER PRIMARY KEY,
                  Name TEXT NOT NULL,
                  Surname TEXT NOT NULL,
                  Initials TEXT NOT NULL,
                  Age INTEGER NOT NULL,
                  DateOfBirth TEXT NOT NULL,
                  UNIQUE(Name, Surname, DateOfBirth))''')
    
    conn.commit()
    conn.close()


def generate_random_date(age):
    """Generate random birth date based on age"""
    today = datetime.now()
    birth_year = today.year - age
    
    month = random.randint(1, 12)
    max_day = 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
    day = random.randint(1, max_day)
    
    return f"{day:02d}/{month:02d}/{birth_year}"


def generate_csv(num_records):
    """Generate CSV file with random data"""
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.csv')
    used_combinations = set()
    
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(['Id', 'Name', 'Surname', 'Initials', 'Age', 'DateOfBirth'])
        
        for i in range(1, num_records + 1):
            while True:
                name = random.choice(NAMES)
                surname = random.choice(SURNAMES)
                age = random.randint(18, 80)
                dob = generate_random_date(age)
                initials = name[0]
                
                combination = (name, surname, age, dob)
                
                if combination not in used_combinations:
                    used_combinations.add(combination)
                    writer.writerow([i, name, surname, initials, age, dob])
                    break
    
    return output_path


def import_csv_to_db(file_path):
    """Import CSV file to SQLite database"""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute('DELETE FROM csv_import')
    
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  
        
        for row in csv_reader:
            c.execute('''INSERT INTO csv_import (Id, Name, Surname, Initials, Age, DateOfBirth)
                        VALUES (?, ?, ?, ?, ?, ?)''', row)
    
    conn.commit()
    record_count = c.execute('SELECT COUNT(*) FROM csv_import').fetchone()[0]
    conn.close()
    
    return record_count


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/view')
def view_data():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        c.execute('SELECT * FROM csv_import')
        records = c.fetchall()
        
        columns = ['ID', 'Name', 'Surname', 'Initials', 'Age', 'Date of Birth']
        
        conn.close()
        return render_template('view.html', records=records, columns=columns)
    
    except Exception as e:
        return f"Error fetching data: {str(e)}", 500



@app.route('/generate', methods=['POST'])
def generate():
    try:
        num_records = int(request.form['num_records'])
        if num_records <= 0:
            return "Number of records must be positive", 400
        
        output_path = generate_csv(num_records)
        return send_file(output_path, as_attachment=True)
    
    except Exception as e:
        return f"Error generating CSV: {str(e)}", 500
    


@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['file']
        if file.filename == '':
            return "No file selected", 400
        
        if not file.filename.endswith('.csv'):
            return "File must be CSV format", 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        record_count = import_csv_to_db(filepath)
        
        return f"Successfully imported {record_count} records"
    
    except Exception as e:
        return f"Error importing CSV: {str(e)}", 500


if __name__ == '__main__':
    create_database()
    # app.run(debug=True)