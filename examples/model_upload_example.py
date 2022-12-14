
'''
Author:
    Sherry Yu (shuang.yu@ibm.com)
Initial Version:
    Aug-2022
Function:
   A simple script showing how to deploy, start, and delete a model.
   It also includes inference using the MNIST model.
   This script needs to be run from the wmla-python-client/examples directory.
'''

from ibm_wmla_client import Connection, update_model_profile_parameters
import numpy as np
import time

service_url = "<URL>"
service_instance = "<SERVICE_INSTANCE_NAME>"

username = "username"
password = "password"

edi_connection = Connection(service_url, service_instance, wmla_v1=True, edi=True,
                 apikey=None, username=username, password=password)

edi_connection.connect()
conn = edi_connection.service_edi

model_name = 'mnisttest'

def delete_model(model_name):
    conn.stop_model_inference(model_name)
    response = conn.get_model_instance(model_name)

    while response.result['state'] != 'disabled':
        time.sleep(1)
        response = conn.get_model_instance(model_name)

    conn.delete_model(model_name=model_name)


def start_model(model_name):
    file_handle = open("mnist_example/mnist.tar", "rb")
    result = conn.deploy_model(userfile = file_handle, timeout = 300)

    response = conn.get_model_profile(model_name)
    model_profile = response.result

    update_model_profile_parameters(model_profile,
                    'shared', 'GPUHosts',
                    '/ANZ/ANZ-DLI-IG/ANZ-DLI-IG-sparkexecutor/ANZ-DLI-IG-sparkexecutor1')

    response = conn.update_model_profile(model_name, model_profile)

    response = conn.start_model_inference(model_name)
    response = conn.get_model(model_name)
    response = conn.get_model_instance(model_name)
    print(response.result)


def infer(model_name):
    response = conn.get_model_instance(model_name)
    print(response.result)

    img_shape = (28, 28, 1)
    x_test = np.random.random_sample((1,) + img_shape)
    x_test = x_test.tolist()

    data = {'id': 0, 'data': x_test}

    response = conn.run_inference(model_name, data)
    print(response)


# delete_model(model_name)
start_model(model_name)

response = conn.get_model(model_name)
print(response.result)

response = conn.get_model_instance(model_name)
print(response.result)

infer(model_name)

