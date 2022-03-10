from redhareapi import Kernel
import json

class InferenceKernel(Kernel):
    def __init__(self, get_model, load_model, preprocess, predict, postprocess, input_structure = None, output_structure = None):
        self.get_model = get_model
        self.load_model = load_model 
        self.preprocess = preprocess ## function
        self.predict = predict
        self.postprocess = postprocess
        self.input_structure = input_structure
        self.output_stucture = output_structure

    #def determine_types(dict_):
    #    type_structure = {}
    #    if isinstance(dict_, dict):
    #        if dict_.get("data"):
    #            data_type_lvl1 dict_.get("data")
    #            if isinstance(data_type_lvl1, dict) or isinstance(data_type_lvl1, list):

    #        for k,v in dict_:
                ## Find types 
    
    def _attributes_to_dict(self, input_):
        if input_:
            {att.get("key"):att.get("value") for att in input_.get("attributes")}
        else:
            return input_

    def _add_attributes(self, dict_, task_context):
        dict_["Version"] = task_context.get_version()
        dict_["Model Name"] = task_context.get_model_name()
        dict_["Task ID"] = task_context.get_id()
        dict_["Session ID"] = task_context.get_session_id()
        return dict_


    def _flatten_tasks(self, task_context):
        data_list = []
        attributes_list = []
        while task_context:
            input_data = json.loads(task_context.get_input_data())
            attributes = self._add_attributes(input_data.get("attributes"), task_context)
            data = input_data.get("data")
            data_list.append(data)
            attributes_list.append(attributes)
            task_context.next()
        return data_list, attributes_list

    def on_kernel_start(self, kernel_context):

        InferenceKernel.log_info("Kernel Start")
        InferenceKernel.log_info("Model Instance ID: " + kernel_context.get_instance_id())

        model_details = json.loads(kernel_context.get_model_description())
        
        InferenceKernel.log_info("Model Input Details: " +  json.dumps(model_details)
        )

        model_path = model_details.get("model_path")
        InferenceKernel.log_info("Model Path Details: " +  model_path)

        self.attributes = self._attributes_to_dict(model_details.get("attributes"))

        InferenceKernel.log_info("Getting Model Path")

        try:
            model_path = self.get_model(model_path, **attributes)
            InferenceKernel.log_info("New Model Path: " + model_path)
        except:
            InferenceKernel.log_error("Failed to get model path")
        try:
            model = self.load_model(model_path, **self.attributes)
        except:
            InferenceKernel.log_error("Failed to load model")

    def on_task_invoke(self, task_context):
        try:
            ## Setup required empty lists to store data 
            ## NOTE task context is an array of dicts 
            ## Two ways to handle this: 1 - flatten data into a list and handle list. 2 - is to loop through the array 
            
            ## data is a array of dictionaries 
            ## flatten tast_context 
            # Expect input_data to have the form {"data": <data here>, "attributes": {<attributes>}}
            data_list, attribute_list = self._flatten_tasks(task_context)

            ## Data gets preprocesssed
            preprocessed_data = self.preprocces(data_list, attribute_list)    
            predicted_result = self.predict(self.model, preprocessed_data, attribute_list)

            output_data = self.postprocess(predicted_results, attribute_list))

            self.task_context.set_output_data(json.dumps(output_data))
        
        except Exception as e:
            InferenceKernel.log_error("-------------------------")
            InferenceKernel.log_error( str(e) )
            task_context.set_output_data("Failed due to: " + str(e))
            InferenceKernel.log_error("-------------------------")


            


