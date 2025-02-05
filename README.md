# CSV Generator and Importer Documentation

## System Requirements
- Python 3.8 or higher
- Flask 2.0 or higher
- SQLite (comes pre-installed with Python)
- Git (optional)

## Setup Instructions

### 1. Setting up a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
virtualenv venv
source venv/bin/activate
```

### 2. Installing Required Packages
After activating the virtual environment, install the required packages using pip:
```bash
pip install -r requirements.txt
```


### 3. Running the Application
1. Start the server:
```bash
python app.py
```

2. Access the application:
- Open your web browser
- Navigate to `http://127.0.0.1:5000`

### 4. Using the Application

#### Generating CSV
1. Navigate to the home page.
2. Enter the number of records you want to generate in the "Number of Records" field.
3. Click "Generate CSV".
4. The generated CSV file will be downloaded automatically.

#### Importing CSV
1. Navigate to the home page.
2. Select a CSV file using the "Select CSV File" button.
3. Click "Import CSV".
4. A success or error message will be displayed based on the import result.

#### Viewing Records
To view all imported records:
1. Start the application.
2. Navigate to `http://127.0.0.1:5000/view` in your web browser.
3. You will see a table displaying all records with their details.

### Database Management
The application uses SQLite to store imported CSV data. The database file (`database.db`) will be created automatically when the application runs for the first time.

## Troubleshooting

### Common Issues and Solutions

1. **Database Connection Error**
   - Ensure that the application has permission to create and write to the `database.db` file in the project directory.

2. **CSV Import Errors**
   - Ensure the CSV file is formatted correctly with the required headers: `Id, Name, Surname, Initials, Age, DateOfBirth`.
   - Check for any empty fields or invalid data types in the CSV file.

3. **Port Already in Use**
   - If you encounter a port conflict, change the port in the `app.run()` method in `app.py`:
   ```python
   app.run(debug=True, port=5001)  # or any other available port
   ```

4. **Permission Denied**
   ```bash
   # Linux/macOS
   sudo chmod +x app.py
   ```
