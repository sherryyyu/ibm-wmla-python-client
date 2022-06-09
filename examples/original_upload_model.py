print("Get token:")
try:
    response = service.get_auth_token()
    token = response.result['user_token']
    print("Token success")
except ApiException as e:
    print("API request failed with status code " + str(e.code) + ": " + e.message)
print("List models:")
try:
    response = service.get_models(token)
    print(response.result)
except ApiException as e:
    print("API request failed with status code " + str(e.code) + ": " + e.message)
print("Deploy model:")
file_handle = open("pingpongnew.tar", "rb")
try:
    response = service.deploy_model(token, userfile=file_handle)
    print(response.result)
except ApiException as e:
    print("API request failed with status code " + str(e.code) + ": " + e.message)
print("Get model profile:")
try:
    response = service.get_model_profile(token, 'pingpongnew')
    model_profile = response.result
    print(response)
except ApiException as e:
    print("API request failed with status code " + str(e.code) + ": " + e.message)
print(model_profile)
modify_model_profile(model_profile,
                'shared', 'GPUHosts',
                '/ANZ/ANZ-DLI-IG/ANZ-DLI-IG-sparkexecutor/ANZ-DLI-IG-sparkexecutor1')
print('Updated model profile: ', model_profile)
print('Upload updated model profile:')
try:
    response = service.update_model_profile(token, 'pingpongnew', model_profile)
    print(response.result)
except ApiException as e:
    print("API request failed with status code " + str(e.code) + ": " + e.message)
print('Start a model:')
try:
    response = service.start_model_inference(token, 'pingpongnew')
    print(response.result)
except ApiException as e:
    print("API request failed with status code " + str(e.code) + ": " + e.message)
print('Stop a model:')
try:
    response = service.stop_model_inference(token, 'pingpongsy')
    print(response.result)
except ApiException as e:
    print("API request failed with status code " + str(e.code) + ": " + e.message)
print('Get the model:')
try:
    response = service.get_model(token, 'pingpongnew')
    print(response.result)
    print('Service URL: ', response.result['service_uri'])
except ApiException as e:
    print("API request failed with status code " + str(e.code) + ": " + e.message)
print('Check model instance status:')
try:
    response = service.get_model_instance(token, 'pingpongnew')
    print(response.result)
except ApiException as e:
    print("API request failed with status code " + str(e.code) + ": " + e.message)
print("Query the model:")
data = {"data" : "12345"}
try:
    response = service.run_inference(token, 'pingpongnew', data)
    print(response.result)
except ApiException as e:
    print("API request failed with status code " + str(e.code) + ": " + e.message)