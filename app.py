import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, DecimalField, FieldList
from wtforms.validators import DataRequired

load_dotenv()


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


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route("/", methods=['GET', 'POST'])
def home():

    transaction = Transaction()
    if transaction.validate_on_submit():
        print("good")

    return render_template('home.html', transaction=transaction)


if __name__ == "__main__":

    app.run()
