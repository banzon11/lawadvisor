from mysite.settings import SECRET_KEY
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
import requests
import json
import datetime
import random, string
import jwt
from api.models import BlackListedToken


def blackListToken(request):
    token = request.headers['Authorization'].split(' ')[1]
    t, created = BlackListedToken.objects.get_or_create(token=token)


def isTokenValid(request):
    token = request.headers['Authorization'].split(' ')[1]
    t = BlackListedToken.objects.filter(token=token)
    if len(t) > 0:
        return False

    return True


def generate(user, username, password):
    payload = {
        "agentId": user.id,
        "username": username,
        "password": password,
    }
    url = settings.TOKEN_URL
    url_response = requests.post(url, payload)
    response = json.loads(url_response.text)
    return response


def decode_token(request):
    token = request.headers['Authorization'].split(' ')[1]
    decoded_token = jwt.decode(token, options={'verify_signature': False})
    return decoded_token


def validate_decoded_token(request):
    decodedToken = decode_token(request)
    user_id = decodedToken['user_id']

    if not isTokenValid(request):
        return False, decodedToken

    try:
        user = User.objects.get(pk=user_id)
        if user:
            return True, decodedToken
    except:
        return False, decodedToken


def set_token_expiry():
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    return str(expiry)


def set_token_iat():
    iat = datetime.datetime.utcnow()
    return str(iat)


def generate_temporary_password():
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits

    long_pwd = lower + upper + num
    temp = random.sample(long_pwd, 10)

    temp_pwd = "".join(temp)

    return temp_pwd
