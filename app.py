import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, DecimalField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired

load_dotenv()


def get_db_connection():
    conn = psycopg2.connect(host=os.environ['DB_HOST'],
                            database=os.environ['DB_NAME'],
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


class ProductEntryForm(FlaskForm):
    product_name = StringField("Product Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    subcategory = StringField("Subcategory", validators=[DataRequired()])
    quantity = DecimalField("Quantity", validators=[DataRequired()])
    unit_price = DecimalField("Unit Price", validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired()])
    notes = StringField("Notes")


class Transaction(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    vendor = StringField("Vendor", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    subtotal = DecimalField("Subtotal", validators=[DataRequired()])
    discount = DecimalField("Discount", validators=[DataRequired()])
    tax = DecimalField("Tax", validators=[DataRequired()])
    tip = DecimalField("Tip", validators=[DataRequired()])
    total = DecimalField("Total", validators=[DataRequired()])
    payment_method = StringField("Payment Method", validators=[DataRequired()])
    notes = StringField("Notes")

    product = FieldList(FormField(ProductEntryForm), min_entries=2)

    add = SubmitField("Add")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route("/", methods=['GET', 'POST'])
def home():

    transaction = Transaction()
    if transaction.validate_on_submit():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO transactions '
                    '(date, vendor, location, subtotal, discount, tax, tip, total, payment_method, notes) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING transaction_id',
                    (transaction.date.data, transaction.vendor.data, transaction.location.data,
                     transaction.subtotal.data, transaction.discount.data, transaction.tax.data,
                     transaction.tip.data, transaction.total.data, transaction.payment_method.data,
                     transaction.notes.data))
        transaction_id = cur.fetchone()

        product_list = [product.data for product in transaction.product.entries]

        for product in product_list:

            cur.execute('INSERT INTO products '
                        '(transaction_id, product_name, category, subcategory, quantity, unit_price, price, notes) '
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                        (transaction_id, product['product_name'], product['category'], product['subcategory'],
                         product['quantity'], product['unit_price'], product['price'], product['notes']))
        conn.commit()
        cur.close()
        conn.close()

    return render_template('home.html', transaction=transaction)


@app.route("/transactions")
def transactions():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM transactions;')
    transaction_data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('transactions.html', transactions=transaction_data)


if __name__ == "__main__":

    app.run()
