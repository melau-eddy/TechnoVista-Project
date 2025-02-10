import requests
from requests.auth import HTTPBasicAuth
import base64
import json
import datetime
from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

# Generate the current timestamp in the format yyyyMMddHHmmss
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# Function to get M-Pesa access token
def get_mpesa_token():
    consumer_key = "UCOLz4IHesReIjmyWswYALA5UWAtlPzKfLZk6H9TSAY0bjIg"
    consumer_secret = "ACbpFsQMikEdGwBIwQX7EglxHsBj26GJJmde42pvMzP2NIaYyHGcp5RK79OuHAMQ"
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        r.raise_for_status()  # Raise an exception for 4XX/5XX status codes
        response_data = r.json()
        if 'access_token' in response_data:
            return response_data['access_token']
        else:
            print(f"Error: {response_data.get('error', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the token: {e}")
        return None

# Flask app setup
app = Flask(__name__)
CORS(app)
api = Api(app)

# Resource to handle STK push requests
class MakeSTKPush(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone', type=str, required=True, help="This field is required")
    parser.add_argument('amount', type=str, required=True, help="This field is required")

    def post(self):
        data = MakeSTKPush.parser.parse_args()
        print(f"Received data: {data}")  # Debugging line

        business_shortcode = "174379"
        online_passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

        # Ensure encode_data is bytes
        encode_data = f"{business_shortcode}{online_passkey}{timestamp}".encode('utf-8')
        passkey = base64.b64encode(encode_data).decode('utf-8')

        try:
            # Get access token
            access_token = get_mpesa_token()
            if not access_token:
                return {
                    "success": False,
                    "message": "Failed to get access token from M-Pesa."
                }, 400

            # STK push request URL
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

            headers = { 
                "Authorization": f"Bearer {access_token}", 
                "Content-Type": "application/json" 
            }

            # Prepare the request body
            request_data = {
                "BusinessShortCode": business_shortcode,
                "Password": passkey,
                "Timestamp": timestamp,  # Include timestamp
                "TransactionType": "CustomerPayBillOnline",
                "Amount": data['amount'],
                "PartyA": data['phone'],
                "PartyB": 174379,
                "PhoneNumber": data['phone'],
                "CallBackURL": "https://mydomain.com/path",
                "AccountReference": "CompanyXLTD",
                "TransactionDesc": "Payment of X"
            }

            # Make the request to the M-Pesa API
            response = requests.post(api_url, json=request_data, headers=headers)

            # Log the response content for debugging
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")

            # If the response is empty or not JSON
            if response.status_code >= 400:
                return {
                    "success": False,
                    "message": f"Error: {response.text}"
                }, 400

            try:
                response_json = response.json()  # Try to parse JSON
            except ValueError:
                return {
                    "success": False,
                    "message": "Error: Received non-JSON response."
                }, 400

            # Return the response from M-Pesa if everything is fine
            return {
                "data": response_json
            }, 200

        except Exception as e:
            print(f"Error occurred: {e}")  # Log the error
            return {
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }, 400

# Setup the API route for STK push
api.add_resource(MakeSTKPush, "/stkpush")

@app.route("/")
def form():
    return render_template("form.html")

if __name__ == "__main__":
    app.run(port=5001, debug=True)
