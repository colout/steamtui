import requests
from activesoup import driver
import bs4
import json
import re
import base64
import time
import npyscreen

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA


def main ():
    ''' 
    Login process as grocked from Steam's unminified login.js (why don't they minify?!):
    
    1)  Get public key for my username from an endpoint.
    2)  
    
    Notes:  
    - Does this mean they are saving passwords encrypted and reversable?!
    - I've never been captcha'd but I saw a recaptcha link.  Login might require javascript in the future, so this isn't futureproof
    - Found this https://gist.github.com/b1naryth1ef/8202642
    '''

    username = ''
    password = ''


    # Replace non-ascii characters
    username = re.sub(r'/[^\x00-\x7F]/g', '', username)
    password = bytes(re.sub('/[^\x00-\x7F]/g', '', password).encode())

    rsa = get_rsa_pub_key(username)
    login (username, password, rsa)

def get_rsa_pub_key (username):
    r = requests.post('https://steamcommunity.com/login/getrsakey',{'username' : username}).json()
    print(r)

    e = int(r['publickey_exp'], 16)
    print (e)
    n = int(r['publickey_mod'], 16)

    return {
        'pubkey': (RSA.construct((n, e))),
        'timestamp': r['timestamp']
    }

def login (username, password, rsa):
    cipher = PKCS1_v1_5.new(rsa['pubkey'])
    h = SHA.new(password)

    encrypted_password = base64.b64encode(cipher.encrypt(password)).decode()
    print(encrypted_password)

    payload = {
        'donotcache': str(int(time.time() * 1000)),
        'password': encrypted_password,
        'username': username,
        'twofactorcode': '',
        'emailauth': '',
        'loginfriendlyname': '',
        'captchagid': '-1',
        'captcha_text': '',
        'emailsteamid': '',
        'rsatimestamp': rsa['timestamp'],
        'remember_login': 'false',
    }

    print (payload)
    exit()
    r = requests.post('https://steamcommunity.com/login/dologin', payload)
    print (r.text)
    print (r.status_code)


if __name__ == "__main__":
    main()

