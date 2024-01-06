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

cur.execute('INSERT INTO transactions '
            '(date, vendor, location, subtotal, discount, tax, tip, total, payment_method, notes) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING transaction_id',
            ('2023-11-18', 'Shoppers Drug Mart', 'Waterloo', 12.98, 0, 0.78, 0, 13.76, 'Tangerine Card', ''))

transaction_id = cur.fetchall()[0]
cur.execute('INSERT INTO products '
            '(transaction_id, product_name, category, subcategory, quantity, unit_price, price, notes) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (transaction_id, 'Made Good Snack', 'Food', 'Groceries', 2, 3.00, 6.00, ''))
cur.execute('INSERT INTO products '
            '(transaction_id, product_name, category, subcategory, quantity, unit_price, price, notes) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (transaction_id, 'Eggs', 'Food', 'Groceries', 2, 3.49, 6.98, ''))

cur.execute('UPDATE transactions '
            'SET date=%s, vendor=%s, location=%s, subtotal=%s, discount=%s, tax=%s, tip=%s, total=%s, '
            'payment_method=%s, notes=%s '
            'WHERE transaction_id=%s',
            ('2023-11-18', 'Shoppers Drug Mart', 'Waterloo', 12.98, 0, 0.78, 0, 13.76,
             'Tangerine Card', 'Sample Comment',
             transaction_id))

cur.execute('UPDATE products '
            'SET product_name=%s, category=%s, subcategory=%s, quantity=%s, unit_price=%s, price=%s, notes=%s '
            'WHERE product_id=%s',
            ('Made Good Snack', 'Food', 'Groceries', 2, 3.00, 6.00, 'Banana Chocolate', 1))

cur.execute('DELETE FROM products WHERE product_id=%s' % 1)

cur.execute('DELETE FROM transactions WHERE transaction_id=%s' % 1)

# Commit operations
conn.commit()

# Close cursor and connections
cur.close()
conn.close()
