

import json
import logging
import os
import sys
import netifaces

from pyfiglet import Figlet

class View:
    def __init__(self, title = 'ICN Stage'):
        self.title = title
    def print_view(self):
        f = Figlet(font='slant')
        print (f.renderText(self.title))

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from Crypto.PublicKey import RSA
import tarfile
import os


class Sundry:

    @staticmethod
    def get_pkey(path):
        with open(path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())

        return pem.decode('utf-8')

    @staticmethod
    def compress_dir(input_dir_, output_file_):
        tar_file = tarfile.open(output_file_, "w:gz")
        current_dir = os.getcwd()
        os.chdir(input_dir_)
        for name in os.listdir("."):
            tar_file.add("%s" % (name))
        tar_file.close()
        os.chdir(current_dir)

    @staticmethod
    def get_ensemble_ips(json_file):
        f = open(json_file)
        data = json.load(f)
        JSON_PORT = None
        JSON_ADRESS = ''

        for i in data['Settings']:
            JSON_PORT = i['ClientPort']

        for i in data['Nodes']: 
            JSON_ADRESS += (i['remote_hostname']+':'+str(JSON_PORT)+',')

        return JSON_ADRESS[:-1]

    @staticmethod
    def get_ip_adapter(adapter):
        return netifaces.ifaddresses(adapter)[netifaces.AF_INET][0]['addr']