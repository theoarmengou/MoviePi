##
# EPITECH PROJECT, 2019
# MoviePi
# File description:
# utils.py
##

import datetime
import jwt
from dbHelper import dbHelper
from userHelper import userHelper

ret_packet = {'responseStatus': 0, 'message': "", 'data': any}
Key = 'MoviePiTheoAudreyHicham'
LEN_MAX_USER = 255

db = dbHelper('moviepi_api', 'moviepi_api', 'moviepi', '51.75.141.254')
userH = userHelper(db, LEN_MAX_USER)


def fill_return_packet(iswork, typeoferror, data):
    ret_packet['responseStatus'] = iswork
    ret_packet['message'] = typeoferror
    ret_packet['data'] = data
    return ret_packet


def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            Key,
            algorithm='HS256'
        ).decode('utf-8')
    except Exception as e:
        return e


def check_auth_token(request):
    auth_headers = request.headers.get('Authorization', '').split()
    if len(auth_headers) != 2:
        return None
    try:
        payload = jwt.decode(auth_headers[1], Key)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    return False