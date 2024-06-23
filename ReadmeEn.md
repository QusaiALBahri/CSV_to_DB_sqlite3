# Script to Convert CSV File to SQLite Database

## Introduction
This script reads a CSV file and converts it into a SQLite database dynamically. The table in the database is created based on the structure of the CSV file, and all data from the CSV file is inserted into the table.

## Requirements
- Python 3
- `sqlite3` library (included in Python)
- `csv` library (included in Python)

## How to Use

1. Provide the path to the CSV file you want to convert.
2. Provide the name of the file where you want to create the SQLite database.
3. Provide the name of the table you want to create in the database.

## Step-by-Step Explanation

1. **Import Required Libraries**:
    - `sqlite3` for handling SQLite database.
    - `csv` for reading the CSV file.

2. **Define a Function to Detect Data Type**:
    - The function `detect_data_type` tries to convert values to `INTEGER` or `REAL`. If it fails, it assumes the value is text (`TEXT`).

3. **Connect to the Database**:
    - Create a connection to the database or create a new database if it doesn't exist.

4. **Read the CSV File**:
    - Open and read the contents of the CSV file.
    - Extract the first row as column headers.
    - Extract a sample row for data type detection.

5. **Detect Data Types**:
    - Detect data types for each column based on the sample row.

6. **Create SQL Query to Create Table**:
    - Build an SQL query to create the table using the extracted column headers and detected data types.

7. **Execute the Create Table Query**:
    - Execute the SQL query to create the table in the database.

8. **Insert Data into the Table**:
    - Build an SQL query to insert data into the table.
    - Insert all rows from the CSV file into the table.

9. **Handle Mismatched Rows**:
    - If a row has a different number of values than the number of columns, skip that row and print a message.

10. **Commit Changes and Close Connection**:
    - Commit the changes to the database.
    - Close the connection to the database.

## Code

```python
import sqlite3
import csv

def csv_to_sqlite(csv_file_path, db_file_path, table_name):
    def detect_data_type(value):
        try:
            int(value)
            return 'INTEGER'
        except ValueError:
            try:
                float(value)
                return 'REAL'
            except ValueError:
                return 'TEXT'
    
    # Connect to the SQLite database
    db = sqlite3.connect(db_file_path)
    cursor = db.cursor()

    # Open the CSV file and read its contents
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Extract the header row
        
        # Check if sample_data is non-empty
        sample_data = next(reader, None)  # Extract a sample row for data type detection

        if sample_data is None:
            print("CSV file is empty.")
            db.close()
            return
        
        # Detect data types
        column_types = [detect_data_type(value) for value in sample_data]

        # Create table query dynamically
        create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ('
        create_table_query += ', '.join([f'"{header}" {col_type}' for header, col_type in zip(headers, column_types)])
        create_table_query += ');'
        
        # Execute the create table query
        cursor.execute(create_table_query)
        
        # Insert data into the table
        insert_query = f'INSERT INTO {table_name} ({", ".join(headers)}) VALUES ({", ".join(["?" for _ in headers])})'
        
        cursor.execute(insert_query, sample_data)  # Insert the sample data first
        for row in reader:
            if len(row) == len(headers):  # Ensure the row has the correct number of columns
                cursor.execute(insert_query, row)
            else:
                print(f"Skipping row due to column mismatch: {row}")
        
        # Commit the changes to the database