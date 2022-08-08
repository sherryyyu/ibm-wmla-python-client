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
<!-- * A simple example to [verify the connection](examples/test_connection.py) -->

## Model Deployment and Inference
```python
model_name = "MODEL_NAME"
model_tar_file_path = "MODEL_TAR_FILE_PATH"
kernel_consumer_path = "KERNEL_CONSUMER_PATH"

# Delete model
'''
- Stop a model: a) we need to stop a model before we delete a model; b) stopping a model doesn't mean it's deleted from WMLA, you can restart by start_model()
- Delete a model: a) permanently deleting a model from WMLA b) to upload again, you'll have to deploy_model()
'''
conn.stop_model_inference(model_name) # stop a specific model
conn.delete_model(model_name) # delete a specific model

# Start model
file_handle = open(model_tar_file_path, "rb")
result = conn.deploy_model(userfile=file_handle, timeout = 300) # upload model package files
response = conn.get_model_profile(model_name) # get application profile for a specific model
model_profile = response.result
update_model_profile_parameters(model_profile, 
                                gpu_type='shared',
                                kernel_resource_group='GPUHosts',
                                kernel_consumer_path=kernel_consumer_path)
print(model_profile)
response = conn.update_model_profile(model_name, **model_profile) # update application profile for a specific model
response = conn.start_model_inference(model_name) # start a specific model
response = conn.get_model(model_name) # get a specific model
print(response.result)
response = conn.get_model_instance(model_name) # get a specific model instance information
print(response.result)

# Infer
data = {'id': 0, 'data': x_test}
response = conn.run_inference(model_name, data) # input data for inference
print(response)

```

## Questions
If you are having difficulties using this SDK or have a question about the IBM Cloud services,
please ask a question
[Stack Overflow](http://stackoverflow.com/questions/ask?tags=ibm-cloud).

## Issues
If you encounter an issue with the project, you are welcome to submit a
[bug report](<github-repo-url>/issues).
Before that, please search for similar issues. It's possible that someone has already reported the problem.

## Open source @ IBM
Find more open source projects on the [IBM Github Page](http://ibm.github.io/)

## Contributing
See [CONTRIBUTING.md](https://github.ibm.com/CloudEngineering/python-sdk-template/blob/master/CONTRIBUTING.md).

## License
This SDK is released under the Apache 2.0 license.
The license's full text can be found in [LICENSE](https://github.ibm.com/CloudEngineering/python-sdk-template/blob/master/LICENSE).

<!-- * A complete example for [uploading, deploying and starting a model](examples/test_model_upload.py) -->

<!-- ## Examples

* A simple example to [verify the connection](examples/test_connection.py)
* A complete example for [uploading, deploying and starting a model](examples/test_model_upload.py) (documentation imcomplete, ask Sherry for details) -->