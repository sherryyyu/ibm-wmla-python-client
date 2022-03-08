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
            model = self.load_model()
        except:
            log("could not load")

        


    def on_task_invoke(self, task_context ):


        ## data is a array of dictionaries 
        
        while task_context:

            self.names
            input_data = json.loads(task_context.get_input_data())
            attributes = input_data.get("attributes")
            input_data = input_data.get("data")

            ## Data gets preprocesssed



            preprocessed_data = self.preprocces(data, **attributes)    
            predicted_result = self.predict(model, preprocessed_data, **attributes)

            output_data = self.postprocess(predicted_result, **attributes))

            ## Preprocessed data goes into predict of model
            ## What is preprocessed_data (whats the format??)


            


            ## Output data gets postprocessed 

            task_context.set_output_data(json.dumps(output_data))
            task_context = task_context.next()
    


