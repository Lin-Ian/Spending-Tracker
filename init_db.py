import os
from dotenv import load_dotenv
import psycopg2

# Load .env file variables
load_dotenv()

# Connect to database
conn = psycopg2.connect(host=os.environ['DB_HOST'],
                        database=os.environ['DB_NAME'],
                        user=os.environ['DB_USERNAME'],
                        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS vendors;')
cur.execute('CREATE TABLE vendors '
            '(vendor_id serial PRIMARY KEY,'
            'date date NOT NULL,'
            'vendor varchar (50) NOT NULL,'
            'location varchar (50) NOT NULL,'
            'subtotal decimal NOT NULL,'
            'tax decimal NOT NULL,'
            'tip decimal NOT NULL,'
            'payment_method varchar (50) NOT NULL,'
            'additional_notes varchar (100));')

# Commit operations
conn.commit()

# Close cursor and connections
cur.close()
conn.close()
