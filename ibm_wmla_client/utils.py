def update_model_profile_parameters(model_profile, 
                gpu_type, kernel_resource_group, kernel_consumer_path):
    model_profile['kernel']['gpu'] = gpu_type
    model_profile['resource_allocation']['kernel']['resource_group'] = kernel_resource_group
    model_profile['resource_allocation']['kernel']['consumer'] = kernel_consumer_path