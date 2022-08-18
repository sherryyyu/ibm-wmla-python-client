'''
Author:
    Sherry Yu (shuang.yu@ibm.com)
Initial Version:
    Aug-2022
Function:
   A simple script showing how to connect to WMLA.
'''

import time
from urllib import response
from ibm_wmla_client import Connection
import numpy as np

service_url = "<URL>"
service_instance = "<SERVICE_INSTANCE_NAME>"
username = "username"
password = "password"

edi_connection = Connection(service_url, service_instance, wmla_v1=True, edi=True,
                 apikey=None, username=username, password=password)

edi_connection.connect()

time.sleep(3)

conn = edi_connection.service_edi

# list models

print(conn.get_models())

model_name = "pingpong"

print(conn.get_model(model_name))

# res = conn.start_model_inference('pingpongnew')

