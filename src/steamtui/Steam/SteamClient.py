import requests
import json
import re
import base64
import time

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA

# Steam Client
class Client:
    # Logs into steam
    def set_creds(self, username, password):
        # Replace non-ascii characters
        Client._username = re.sub(r'/[^\x00-\x7F]/g', '', username)
        Client._password = bytes(re.sub('/[^\x00-\x7F]/g', '', password).encode())

    def login(self):
        Client._rsa = _get_rsa_pub_key (Client._username)

        response = Client._dologin(self)

        print (self._username)
        print (self._password)

        return response


    def _dologin(self):
        cipher = PKCS1_v1_5.new(Client._rsa['pubkey'])
        h = SHA.new(Client._password)

        encrypted_password = base64.b64encode(cipher.encrypt(Client._password)).decode()

        payload = {
            'donotcache': str(int(time.time() * 1000)),
            'password': encrypted_password,
            'username': Client._username,
            'twofactorcode': '',
            'emailauth': '',
            'loginfriendlyname': '',
            'captchagid': '-1',
            'captcha_text': '',
            'emailsteamid': '',
            'rsatimestamp': Client._rsa['timestamp'],
            'remember_login': 'false',
        }

        return {
            "success":False,
            "requires_twofactor":False,
            "message":"",
            "emailauth_needed":True,
            "emaildomain":"example.com",
            "emailsteamid":"XXXXXXXXXXXXX"
        }

        r = requests.post('https://steamcommunity.com/login/dologin', payload)
        return r.text.json


#
# Ephemeral Helper Functions
#

# Returns public key from Steam's rsa endpoint
def _get_rsa_pub_key (username):
    r = requests.post('https://steamcommunity.com/login/getrsakey',{'username' : username}).json()
    e = int(r['publickey_exp'], 16)
    n = int(r['publickey_mod'], 16)

    return {
        'pubkey': (RSA.construct((n, e))),
        'timestamp': r['timestamp']
    }

