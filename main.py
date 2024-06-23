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
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Extract the header row
        sample_data = next(reader)  # Extract a sample row for data type detection

        # Detect data types
        column_types = [detect_data_type(value) for value in sample_data]

        # Create table query dynamically
        create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ('
        create_table_query += ', '.join([f'{header} {col_type}' for header, col_type in zip(headers, column_types)])
        create_table_query += ');'

        # Execute the create table query
        cursor.execute(create_table_query)

        # Insert data into the table
        insert_query = f'INSERT INTO {table_name} ({", ".join(headers)}) VALUES ({", ".join(["?" for _ in headers])})'

        cursor.execute(insert_query, sample_data)
        for row in reader:
            cursor.execute(insert_query, row)

        # Commit the changes to the database
        db.commit()

    # Close the database connection
    db.close()

    print('Database created and data inserted successfully.')

# Example usage
csv_file_path = 'ddinter_downloads_code_A.csv'
db_file_path = 'Dynamic_Database.db'
table_name = 'Medication'

csv_to_sqlite(csv_file_path, db_file_path, table_name)