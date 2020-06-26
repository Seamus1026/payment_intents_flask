Overview
This app implements the accept a payment workflow from the Stripe docs using Python (flask) and Stripe elements.

Setup

1. install virtual env: pip install virtualenv 
2. create virtual env: virtualenv env 
3. activate the environment: source env/bin/activate
4. install the requirements: pip install requirements.txt
5. run app1.py

The server runs on port 5000. You can navigate to http://localhost:5000 

Test the webhooks / view successful order log

1. Install the Stripe CLI: see step 1 at https://stripe.com/docs/stripe-cli
2. Login with your stripe account: stripe login
3. Open terminal and run: ./stripe listen --forward-to http://localhost:5000/webhook --events=payment_intent.succeeded --events=payment_intent.payment_failed

Once webhooks are set up, successful orders (and failed payment attempts) will be logged in "fulfillment.txt". 