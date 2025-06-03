import os,base64, requests
from datetime import datetime
from django.shortcuts import render
from .forms import PaymentForm
from dotenv import load_dotenv

# Create your views here.
load_dotenv()

#retrieving variables from the env file
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')
MPESA_BASE_URL = os.getenv('MPESA_BASE_URL')
CALLBACK_URL = os.getenv('CALLBACK_URL')

#generate M-pesa access token
def generate_access_token():
    try:
        credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
            headers=headers
        ).json()

        if "access_token" in response:
            return response["access_token"]
        else:
            raise Exception("Failed to generate access token")
    except requests.RequestException as e:
        print(f"Failed to connect to M-Pesa: {str(e)}")


#Initiating the STK Push request and handling the response
def initiate_stk_push(phone_number, amount):
    try:
        token = generate_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        stk_password = base64.b64encode(
            f"{MPESA_SHORTCODE}{MPESA_PASSKEY}{timestamp}".encode()
            
            ).decode()
        
        request_body = {
            'BusinessShortCode': MPESA_SHORTCODE,
            'Password': stk_password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': MPESA_SHORTCODE,
            'PhoneNumber': phone_number,
            'CallBackURL': CALLBACK_URL,
            'AccountReference': 'CompanyXLTD',
            'TransactionDesc': 'Payment of X'
        }

        response = requests.post(
            f"{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
            headers=headers,
            json=request_body
        ).json()

        return response
    
    except requests.RequestException as e:
        print(f"Failed to initiate STK Push: {str(e)}")

        

def index(request):
    form = PaymentForm()
    return render(request, 'index.html', {'form': form})


