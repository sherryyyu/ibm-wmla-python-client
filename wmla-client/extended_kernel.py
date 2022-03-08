from redhareapi import Kernel
import json




def preprocess(data, denoise=True, X_IMG_SIZE=500, Y_IMG_SIZE=400, **kwargs):
    IMG_SIZE = kwargs.get("X_IMG_SIZE")
    preprocess()
    return processed_data

def get_model(model_path):
    if model_path == "URL":
        download
    else:
        return model_path 

def load_model(model_path):
    model = load_tf_model(model_path)
    return model


def predict(model, prepocessed_data):
    # Do stuff 
    input_one = preprocessed_data[0]
    model1, model2 = model
    myown_special_predict_func(model1, model2, preprocessed_data)

    return predicted_output

input_structure = {"data": [1.2,3.2,4.5], "attributes": {"img_size": 500, "denoise": True}}


class InferenceKernel(Kernel):
    def __init__(self, get_model, load_model, preprocess, predict, postprocess, input_structure, output_structure, attributes):
        self.get_model = get_model
        self.load_model = load_model 
        self.preprocess = preprocess ## function
        self.predict = predict
        self.postprocess = postprocess
        self.input_structure = input_structure

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



        ## Preprocess functions has an abitary number of inputs and outputs  



    def wrapper_func(func): 
        def new_func(input_data):
            ## args =  [[1,2,3], [2,3,4]] *args data1 [1,2,3], data2 [2,3,4]
            kwargs = input_data ## **kwargs = {data : [1,2,3], denoise:True, X_IMG_SIZE:500, Y_IMG_SIZE:400, depth=32}
            return func(**kwargs)
        return new_func

    def on_kernel_start(self, kernel_context):

        model_details = json.loads(kernel_context.get_model_description())
        model_path = model_details.get("model_path")
        self.attributes = self._attributes_to_dict(model_details.get("attributes"))

        try:
            model_path = self.get_model(model_path, **attributes)
        except:
            log("Failed to get path")
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
    


