# wmla-python-client
A python based client to simplify using Watson Machine Learning Accelerator 

## Prerequisites

* Python 3.5.3 or above.
* [ibm_wmla](https://github.ibm.com/anz-tech-garage/wmla-python-sdk)


## Installation 

To install the package for debugging:

```
pip install requirements.txt
python setup.py develop
```

To install the package:

```
pip install requirements.txt
pip install .
```

## Setting up WMLA service
```python
from ibm_wmla_client import Connection

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

```
<!-- * A simple example to [verify the connection](examples/test_connection.py) -->

## Model Deployment and Inference
```python
model_name = "MODEL_NAME"
model_tar_file_path = "MODEL_TAR_FILE_PATH"
kernel_consumer_path = "KERNEL_CONSUMER_PATH"

# Start model
file_handle = open(model_tar_file_path, "rb")

# upload model package files
result = conn.deploy_model(userfile=file_handle, timeout = 300) 

# get application profile for a specific model
response = conn.get_model_profile(model_name) 
model_profile = response.result

# change GPU type
model_profile['kernel']['gpu'] = gpu_type

# update application profile for a specific model
response = conn.update_model_profile(model_name, model_profile) 

# start a specific model
response = conn.start_model_inference(model_name) 

# check the model parameters
response = conn.get_model(model_name) 

# check the model status
response = conn.get_model_instance(model_name) 

# Infer
data = {'id': 0, 'data': x_test} # input data for inference
response = conn.run_inference(model_name, data) 

```

## Model clean up

To stop a model: 
```
conn.stop_model_inference(model_name)
```

* You need to stop a model before we delete a model
* It doesn't mean the model is deleted from WMLA
* You can restart by `start_model_inference` after stopping the model



To delete a model:
```
conn.delete_model(model_name)
```

* It permanently delete a model from WMLA 
* To upload again, you'll have to redeploy the mode with `deploy_model`

<!-- Deploy a model: 

Update a model: -->

## Resources

- [Installation instructions](cp4d_offline_install) for the IBM Cloud Pak for Data WMLA Cartridge environment 
- [MNIST example](examples/mnist_example/mnist)
- How to [debug on your local machine](examples/mnist_example/local_debug_example)
- Simple Python scripts for making WMLA EDI [connections](examples/connection_example.py) and [deploying a model](examples/model_upload_example.py)
- Example [Jupyter Notebooks](notebooks) for the WMLA CP4D cartridge environment 
- [How to write kernel.py](examples/README.md)



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
