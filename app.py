import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, DecimalField, FieldList
from wtforms.validators import DataRequired

load_dotenv()


def get_db_connection():
    conn = psycopg2.connect(host=os.environ['DB_HOST'],
                            database=os.environ['DB_NAME'],
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


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


class Product(FlaskForm):
    product_name = StringField("Product Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    subcategory = StringField("Subcategory", validators=[DataRequired()])
    quantity = DecimalField("Quantity", validators=[DataRequired()])
    unit_price = DecimalField("Unit Price", validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired()])
    notes = StringField("Notes")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route("/", methods=['GET', 'POST'])
def home():

    transaction = Transaction()
    product = Product()
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
        cur.execute('INSERT INTO products '
                    '(transaction_id, product_name, category, subcategory, quantity, unit_price, price, notes) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    (transaction_id, product.product_name.data, product.category.data, product.subcategory.data,
                     product.quantity.data, product.unit_price.data, product.price.data, product.notes.data))
        conn.commit()
        cur.close()
        conn.close()

    return render_template('home.html', transaction=transaction, product=product)


if __name__ == "__main__":

    app.run()
