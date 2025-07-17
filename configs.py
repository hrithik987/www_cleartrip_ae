# Dependencies
import pymysql
import secret_details
import os

# For Multi Threading
THREADING = True
THREADS = 10
PARTS = 1
WAIT = 0.5
TIMEOUT = 10

# For Page Saving
PAGE_DIR = "pages/"

# For Output
OUTPUT_DIR = "output/"


def page_save(ids_path, file_name, data):
    os.makedirs(ids_path, exist_ok=True)
    file_name = os.path.join(ids_path, file_name)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(data)

class sqlDatabase:
    host = secret_details.HOST
    user = secret_details.USER
    password = secret_details.PASSWORD

    # create connection
    def create_connection(self):
        db_config = {
            'host': self.host,
            'user': self.user,
            'password': self.password,
        }
        conn = pymysql.connect(**db_config)
        return conn

    def create_database(self, conn, db_name):
        cursor = conn.cursor()
        cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {db_name};""")
        conn.commit()

    # create table
    def create_table(self, conn, db_name, table_name, columns):
        cursor = conn.cursor()
        cursor.execute(f"USE {db_name};")
        # Construct the field definitions string from the dictionary
        fields_str = ", ".join([f"{field} {type}" for field, type in columns.items()])
        # SQL query to create the table
        create_table_sql = f"""
              CREATE TABLE IF NOT EXISTS {table_name} (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  {fields_str}
              );
              """
        cursor.execute(create_table_sql)
        conn.commit()

    def fetch_data(self, conn, db_name, query):
        cursor = conn.cursor()
        cursor.execute(f"USE {db_name};")
        cursor.execute(query)
        conn.commit()
        return cursor.fetchall()

    def insert_data(self, conn, db_name, table_name, columns, values):
        cursor = conn.cursor()
        cursor.execute(f"USE {db_name};")
        # Construct the column names and values for the SQL query
        columns_str = ", ".join(columns)
        values_str = ", ".join(["%s"] * len(values))  # For parameterized query
        # Construct the insert SQL query
        insert_sql = f"""
              INSERT INTO {table_name} ({columns_str})
              VALUES ({values_str});
              """
        # Execute the query with the actual values
        cursor.execute(insert_sql, tuple(values))
        conn.commit()

    def update_data(self, conn, db_name, query):
        cursor = conn.cursor()
        cursor.execute(f"USE {db_name};")
        cursor.execute(query)
        conn.commit()











