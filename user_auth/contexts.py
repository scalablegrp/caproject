from . import decode_jwt
import base64
import requests

from env import COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET, COGNITO_REDIRECT_URL, COGNITO_TOKEN_ENDPOINT

# Method to retrieve user identifier from cognito if they are logged in
def determine_if_logged_in(request):
    # Context needs to return a dictionary so user needs to be assigned, this will either return dictionary containing cognito details or empty dictionary
    user = request.session.get('cognito_details', {})
    # Only do if block below if the code parameter exists in the url AND the user hasn't already got a code, Otherwise return empty user dictionary
    if request.GET.get('code') != None and len(user) <= 0:
        try:
            # Encode the Cognito Keys
            cognito_key_value = base64.b64encode(bytes(f"{COGNITO_CLIENT_ID}:{COGNITO_CLIENT_SECRET}", "ISO-8859-1")).decode('ascii')
            # Create the content that will be sent to the cognito token endpoint
            header = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f"Basic {cognito_key_value}",
            }
            body = {
                'grant_type': 'authorization_code',
                'client_id': COGNITO_CLIENT_ID,
                'code' : request.GET.get('code'),
                'redirect_uri': COGNITO_REDIRECT_URL, 
            }
            #Get the returned token id from the cognito request and use it as an argument for lambda_handler function
            fetched_token_id = requests.post(COGNITO_TOKEN_ENDPOINT, data=body, headers=header)
            token_id = fetched_token_id.json()['id_token']
            user_data = decode_jwt.lambda_handler(token_id)
            # Create a user dictionary using details from lambda_handler return
            user = {
                'id_token':token_id,
                'name': user_data['name'],
                'email': user_data['email']
            }
            # Add the user info to the django session
            request.session['cognito_details'] = user
            request.session.modified = True
        except Exception as e:
            print(f"There was an issue linking with cognito\n{e}")
    return user




