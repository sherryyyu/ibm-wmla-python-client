from ibm_wmla_client import Connection, update_model_profile_parameters

service_url = "http://wmla-mgmt1.sls30lab.com:9000"
service_instance = "ANZ-DLI-IG"
username = "jbtang"
password = "demoexec"

edi_connection = Connection(service_url, service_instance, wmla_v1=True, edi=True,
                 apikey=None, username=username, password=password)

edi_connection.connect()

conn = edi_connection.service_edi

# conn.stop_model_inference('mnisttest')
# conn.delete_model(model_name='mnisttest')

model_name = 'pingpong4'

# file_handle = open("mnist_example/pingpong4.tar", "rb")
# result = conn.deploy_model(userfile=file_handle)


# response = conn.get_model_profile(model_name)
# model_profile = response.result

# update_model_profile_parameters(model_profile,
#                 'shared', 'GPUHosts',
#                 '/ANZ/ANZ-DLI-IG/ANZ-DLI-IG-sparkexecutor/ANZ-DLI-IG-sparkexecutor1')

# # print('Updated model profile: ', model_profile)


# kernel = model_profile['kernel']
# name = model_profile['name']
# type = model_profile['type']
# policy = model_profile['policy']
# replica = model_profile['replica']
# resource_allocation = model_profile['resource_allocation']
# schema_version = model_profile['schema_version']
# create_time = model_profile['create_time']
# last_update_time = model_profile['last_update_time']

# response = conn.update_model_profile(model_name, kernel = kernel, name = name, policy = policy, 
#                                         replica = replica, resource_allocation = resource_allocation,
#                                         schema_version = schema_version, type = type, 
#                                         create_time = create_time, last_update_time = last_update_time)

# response = conn.get_model_profile(model_name)

# response = conn.start_model_inference(model_name)
# response = conn.get_model(model_name)
# print(response.result)


response = conn.get_model_instance(model_name)
print(response.result)

data = {"data" : "12345"}
response = conn.run_inference(model_name,data)
print(response.result)