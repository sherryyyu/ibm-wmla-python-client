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
