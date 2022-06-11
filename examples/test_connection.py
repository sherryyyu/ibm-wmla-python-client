from urllib import response
from ibm_wmla_client import Connection
import numpy as np

service_url = "http://wmla-mgmt1.sls30lab.com:9000"
service_instance = "ANZ-DLI-IG"
username = "jbtang"
password = "demoexec"

edi_connection = Connection(service_url, service_instance, wmla_v1=True, edi=True,
                 apikey=None, username=username, password=password)

edi_connection.connect()

conn = edi_connection.service_edi

print(conn.get_model("pingpongnew"))

# res = conn.start_model_inference('pingpongnew')

