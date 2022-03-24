from email.mime import base
from multiprocessing import context
import re
from urllib import response
from django.shortcuts import render
from . import decode_jwt
import os
import base64
import requests

from env import CLIENT_ID, CLIENT_SECRET, REDIRECT_URL, TOKEN_ENDPOINT

# Create your views here.
# Method to display the application home page
def display_home_page(request):
    context = {}
    try:
        code = request.GET.get('code')
        userData = getTokens(code)
        # context['given_name'] = userData['given_name']
        context['email'] = userData['email']
        context['status'] = 1

        response = render(request, 'index.html', context)
        response.set_cookie('sessiontoken', userData['id_token'], max_age=60*60, httponly=True)
        # Gather recommendations
        return response
    except:
        token = getSession(request)
        if token is not None:
            userData = decode_jwt.lambda_handler(token, None)
            # context['given_name'] = userData['given_name']
            context['email'] = userData['email']
            context['status'] = 1
            return render(request, 'index.html', context)
        return render(request, 'index.html', {'status': 0})

def getTokens(code):

    if os.path.exists("env.py"):
        import env as env_variables

    TOKEN_ENDPOINT = env_variables.get_token_endpoint()
    REDIRECT_URI = env_variables.get_redirect_url()
    CLIENT_ID = env_variables.get_client_id()
    CLIENT_SECRET = env_variables.get_client_secret()

    encodedData = base64.b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", "ISO-8859-1")).decode("ascii")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encodedData}'
    }

    body = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(TOKEN_ENDPOINT, data=body, headers=headers)

    id_token = response.json()['id_token']
    userData = decode_jwt.lambda_handler(id_token, None)

    if not userData:
        return False

    user = {
        'id_token' : id_token,
        # 'given_name' : userData['given_name'],
        # 'family_name' : userData['family_name'],
        'email' : userData['email']
    }

    return user


def getSession(request):
    try:
        response = request.COOKIES['sessiontoken']
        return response
    except:
        return None


def logout(request):
    response = render(request, 'index.html', {'status': 0})
    response.delete_cookie('sessiontoken')
    return response