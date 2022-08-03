# wmla-python-client
A python based client to simplify using Watson Machine Learning Accelerator 

## Prerequisites

* Python 3.5.3 or above.
* [ibm_wmla](https://github.ibm.com/anz-tech-garage/wmla-python-sdk)


## Installation 

To install the package for debugging (recommended for now):

```
python setup.py develop
```

To install the package:

```
pip install .
```

## Setting up WMLA service
```python
from ibm_wmla_client import Connection, update_model_profile_parameters

service_url = "YOUR_SERVICE_URL:PORT"
service_instance = "YOUR_INSTANCE_NAME"
username = "YOUR_UNAME"
password = "YOUR_PW"

edi_connection = Connection(service_url, service_instance, wmla_v1=True, edi=True,
                 apikey=None, username=username, password=password)

edi_connection.connect()

conn = edi_connection.service_edi

# List models
response = conn.get_models()
print(response.result)

```
* A simple example to [verify the connection](examples/test_connection.py)

## Testing WMLA service
```python
from test_model_upload import delete_model, start_mode, infer
model_name = 'mnisttest'

delete_model(model_name)
start_model(model_name)
infer(model_name)
```

* A complete example for [uploading, deploying and starting a model](examples/test_model_upload.py)

<!-- ## Examples

* A simple example to [verify the connection](examples/test_connection.py)
* A complete example for [uploading, deploying and starting a model](examples/test_model_upload.py) (documentation imcomplete, ask Sherry for details) -->