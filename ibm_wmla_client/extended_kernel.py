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
    
    def install_modules(self):
        pass
    
    def load_modules(self):
        pass

    def get_model(self, model_path, **kwargs):
        return model_path
    
    def load_model(self, model_path, **kwargs):
        ## load_model_code
        pass

    def preprocces(self, data_list, attribute_list, model = None, **kwargs):
        ## preprocessing code here
        pass

    def postprocess(self, predicted_results, attribute_list, **kwargs):
        pass

    def predict_func(self, model, batched_data, batched_attributes, **kwargs):
        pass


    def predict(self, model, preprocessed_data, attribute_list, **kwargs):
        if kwargs.get("batch_size") is not None:
            batch_size = kwargs.get("batch_size")
            data_len = len(preprocessed_data)
            cycles = int(data_len / kwargs.get("batch_size"))
            batched_data = []
            batched_attributes = []
            for a in range(0, cycles):
                batch_min_slice = a*batch_size
                batch_max_slice = (a+1)*batch_size
                batched_data.append(preprocessed_data[batch_min_slice, batch_max_slice])
                batched_attributes.append(attribute_list[batch_min_slice, batch_max_slice])
        else:
            batched_data = preprocessed_data
            batched_attributes = attribute_list
        
        batched_combined = zip(batched_data, batched_attributes)
        for data, attributes in batched_combined:
            predicted_output = self.predict(model, data, attributes, **kwargs)
            postprocessed_output = self.postprocess(predicted_output, attributes, **kwargs)
            self.task_context.set_output_data(json.dumps(output_data))

 
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

        try: 
            self.install_modules()
            self.import_modules()
        except Exception as e:
            InferenceKernel.log_error("-------------------------")
            InferenceKernel.log_error( str(e) )
            task_context.set_output_data("Failed due to: " + str(e))
            InferenceKernel.log_error("-------------------------")

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
            self.model = self.load_model(model_path, **self.attributes)
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
            preprocessed_data = self.preprocces(data_list, attribute_list, model=self.model, **self.attributes)    
            predicted_results = self.predict(self.model, preprocessed_data, attribute_list, **self.attributes)
        
        except Exception as e:
            InferenceKernel.log_error("-------------------------")
            InferenceKernel.log_error( str(e) )
            task_context.set_output_data("Failed due to: " + str(e))
            InferenceKernel.log_error("-------------------------")


            



