# How to write model.json
A `model.json` describes the metadata of the model, and needs to include the following  

- name: model name, eg. 'mnistmodel'
- tag: tags for the model, eg. 'keras'
- model_path: relative path to the model folder (optional)
- weight_path: relative path to the model.h5 file  
- runtime: name of the model runtime
- kernel_path: relative path of the kernel.py file
- schema_version: version number

Below is an example:

```json
{
    "name" : "model name",
    "tag" : "model tags",
    "weight_path" : "path_to_model/model.h5",
    "runtime" : "dlipy3",
    "kernel_path" : "path_to_model/kernel.py",
    "schema_version" : "1"
}
```

# How to write kernel.py
The kernel run function consists of on_kernel_start(), on_task_invoke(), on_kernel_shutdown() in redhareapi.py. The first two functions should be implemented in kernel.py. The run function can make you load model and save output.

## on_kernel_start()
This function runs once when you start the model using the Python client. In this function, you should load the model.

### To load model
```python

# load model.json
model_desc = json.loads(kernel_context.get_model_description())

# get model path
model_path = model_desc['model_path']
model_path = model_path + '/' + model_desc['weight_path']

# load the model
model = tf.keras.models.load_model(model_path)
```

We can get the model path from the `model.json` file which can be loaded by `KernelContext.get_model_description()`. If 'model_path' is not specified in `model.json`, the current working directory will be used as model_path by default. The model path is completed by appending 'model_path' to 'weight_path'. Then, we can load model from the model_path.

<!-- ### To predict on test sample and measure the elapsed time
```python
import time
start = time.time()
y_keras = model.predict(x_test)
end = time.time()
Keras_time = end - start
```
We can check the elapsed time by the difference before and after the prediction -->

## on_task_invoke()

This function runs every time a inference query is made.

You can save output in this function, and this task is executed until the batch size is exhausted.

### To load input data
```python
input_data = json.loads(task_context.get_input_data())
img_id = input_data['id']
img_data = input_data['data']
img_data = np.asarray(img_data).astype('float32')
```
Each time we load the previously prepared `model.json`. Limits the number of loops to batches by decrementing batch by one for each load in `task_context.get_input_data()` function.

### To predict on input data and save output
```python
# predict using the model
y_keras = model.predict(img_data)

# postprocess the model output
output_data = {}
output_data['key'] = img_id
output_data['data'] = y_keras.tolist()

# tell WMLA which variable to return to inference requests
task_context.set_output_data(json.dumps(output_data))
task_context = task_context.next()
```

Executes a loop as much as the batch size by returning the instance decremented by 1 in `task_context.next()` function until batch becomes zero. The output data will be saved by `task_context.set_output_data()` function.


Finally, `kernel.py` should look like: 

```python
class TestKernel(Kernel):
    def on_kernel_start(self, kernel_context):
        try:
            Kernel.log_info("kernel input: " + kernel_context.get_model_description())

            # load model.json
            model_desc = json.loads(kernel_context.get_model_description())
            model_path = model_desc['model_path']
            if model_path == '':
                model_path = os.getcwd()
            Kernel.log_info("currect dir" + os.getcwd())
            
            # get model path
            model_path = model_path + '/' + model_desc['weight_path']

            # load the keras model
            self.model = tf.keras.models.load_model(model_path)

        except Exception as e:
            Kernel.log_error(str(e))
            
    def on_task_invoke(self, task_context):
        try:
            start = time.time()
            Kernel.log_info('on_task_invoke')
            while task_context != None:
                
                # load model input
                input_data = json.loads(task_context.get_input_data())
                img_id = input_data['id']
                img_data = input_data['data']
                
                # preprocess input
                img_data = np.asarray(img_data).astype('float32')
                
                # predict using the loaded model
                y_keras = self.model.predict(img_data)
                
                # postprocess model output
                output_data = {}
                output_data['key'] = img_id
                output_data['data'] = y_keras.tolist()

                # tell WMLA EDI which variable to return to user 
                task_context.set_output_data(json.dumps(output_data))
                
                # next batch
                task_context = task_context.next()
                
            end = time.time()
            Kernel.log_info("exit on_task_invoke, using time %.2f" % (end-start))
        except Exception as e:
            task_context.set_output_data(str(e))
            Kernel.log_error(str(e))

if __name__ == '__main__':
    ppkernel = TestKernel()
    ppkernel.run()
```

