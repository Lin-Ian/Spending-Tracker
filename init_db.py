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

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS products;')
cur.execute('CREATE TABLE products '
            '(product_id serial PRIMARY KEY,'
            'vendor_id integer,'
            'product_name varchar (50) NOT NULL,'
            'category varchar (50) NOT NULL,'
            'subcategory varchar (50) NOT NULL,'
            'quantity integer DEFAULT 1,'
            'unit_price decimal NOT NULL,'
            'price decimal NOT NULL,'
            'additional_notes varchar (100),'
            'FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id))'
            )

# Commit operations
conn.commit()

# Close cursor and connections
cur.close()
conn.close()
