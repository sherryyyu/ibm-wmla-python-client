import time
from urllib import response
from ibm_wmla_client import Connection
import numpy as np

service_url = "http://wmla-mgmt1.sls30lab.com:9000"
service_instance = "ANZ-DLI-IG"
username = "UNAME"
password = "PASSWORD"

edi_connection = Connection(service_url, service_instance, wmla_v1=True, edi=True,
                 apikey=None, username=username, password=password)

edi_connection.connect()

time.sleep(3)

conn = edi_connection.service_edi

# list models

print(conn.get_models())

model_name = "pingpongnew"

print(conn.get_model(model_name))

# res = conn.start_model_inference('pingpongnew')

