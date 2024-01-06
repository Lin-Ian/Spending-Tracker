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
cur.execute('DROP TABLE IF EXISTS transactions CASCADE;')
cur.execute('CREATE TABLE transactions '
            '(transaction_id serial PRIMARY KEY,'
            'date date NOT NULL,'
            'vendor varchar (50) NOT NULL,'
            'location varchar (50) NOT NULL,'
            'subtotal decimal NOT NULL,'
            'tax decimal NOT NULL,'
            'tip decimal NOT NULL,'
            'total decimal NOT NULL,'
            'payment_method varchar (50) NOT NULL,'
            'notes varchar (100));')

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS products CASCADE;')
cur.execute('CREATE TABLE products '
            '(product_id serial PRIMARY KEY,'
            'transaction_id integer,'
            'product_name varchar (60) NOT NULL,'
            'category varchar (50) NOT NULL,'
            'subcategory varchar (50) NOT NULL,'
            'quantity integer DEFAULT 1,'
            'unit_price decimal NOT NULL,'
            'price decimal NOT NULL,'
            'notes varchar (100),'
            'FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE)'
            )

# Commit operations
conn.commit()

# Close cursor and connections
cur.close()
conn.close()
