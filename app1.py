import os
import random
import datetime

from flask import Flask, request, redirect, render_template
from flask_restful import Api
import stripe


app1 = Flask(__name__)
api = Api(app1)

# define dynamically using this
# stripe.api_key = os.getenv("STRIPE_SK")
stripe.api_key = 'sk_test_YOENa4GPKlAA1wxrvHTQ8IRf00K8VBCgGc'   # add test SK here

@app1.route("/")
def home():
    return render_template(
        "index.html",
    )


@app1.route("/webhook",  methods=["POST"])
def webhook():
    orders_file = open("fulfillment.txt", "a")
    payload = request.get_json()
    timestamp = datetime.datetime.fromtimestamp(payload["created"]).strftime('%c')
    if payload["type"] == "payment_intent.succeeded":
        orders_file.write("Intent ID: " + payload["id"] + "\n")
        orders_file.write("Timestamp: " + timestamp + "\n")
        orders_file.write("Order status: successful, fulfillment required." + "\n")
    elif payload["type"] == "payment_intent.payment_failed":
        orders_file.write("Intent ID: " + payload["id"] + "\n")
        orders_file.write("Timestamp: " + timestamp + "\n")
        orders_file.write("Order status: this payment attempt failed, no fulfillment required." + "\n")
    orders_file.close()
    return "ok", 200


@app1.route("/purchase", methods=["POST"])
def accept_payment():
    customer = stripe.Customer.create(
        email=request.form["customerEmail"]
    )

    order_id = random.randint(199, 5999)
    intent = stripe.PaymentIntent.create(
        customer=customer.id,
        amount=request.form["productPrice"].replace(".", ""),
        currency='usd',
        payment_method_types=['card'],
        description="onlinePurchase",
        setup_future_usage="on_session",
        receipt_email=request.form["customerEmail"],
        metadata={
            "integration_check": "accept_a_payment",
            "order_id": order_id,
            "product": request.form["productTitle"],
            "shipping": "Pick-up"
        }
    )

    return render_template(
        "accept_payment.html",
        # define dynamically using this
        # stripe_pk=os.getenv("STRIPE_PK"),
        client_secret=intent.client_secret,
        productTitle=request.form["productTitle"],
        amount=request.form["productPrice"],
        customerName=request.form["customerName"]
    )


@app1.route("/done", methods=["GET"])
def thankyou_page():
    return render_template("payment_confirmation.html")


if __name__ == "__main__":
    app1.run(host="0.0.0.0", debug=True)