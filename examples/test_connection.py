from ibm_wmla_client import Connection

service_url = "http://wmla-mgmt1.sls30lab.com:9000"
service_instance = "ANZ-DLI-IG"
username = "jbtang"
password = "demoexec"
c = Connection(service_url, service_instance, wmla_v1=True, edi=True,
                 apikey=None, username=username, password=password, edi_url=service_url)

c.connect()

conn = c.service_edi

print(conn.get_models())