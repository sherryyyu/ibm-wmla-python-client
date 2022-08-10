# README of kernel.py
The Kernel run function consists of on_kernel_start(),on_task_invoke(),on_kernel_shutdown() in redhareapi.py. The first two functions should be implemented in kernel.py.

## on_kernel_start()
### To load model
```python
from ibm_wmla_client.redhareapi import Kernel
from ibm_wmla_client.redhareapi import KernelContext
kernel_context = KernelContext()
model_desc = json.loads(kernel_context.get_model_description())
model_path = model_desc['model_path']
model_path = model_path + '/' + model_desc['weight_path']
model = tf.keras.models.load_model(model_path)
```
We can get the model path from the model.json file which can be loaded by `KernelContext.get_model_description()`. If 'model_path' is not specified in model.json, the current working directory will be used as model_path by default. The model path is completed by appending 'model_path' to 'weight_path'. Then, we can load model from the model_path.

### To generate test sample
```python
img_shape = (28, 28, 1)
x_test = np.random.random_sample((1,) + self.img_shape)
```
A random test sample is generated with the image size (28,28,1)

### To predict on test sample and measure the elapsed time
```python
import time
start = time.time()
y_keras = model.predict(x_test)
end = time.time()
Keras_time = end - start
```
We can check the elapsed time by the difference before and after the prediction

## on_task_invoke()
This task is executed until the batch size is exhausted.

### To load input data
```python
task_context = TaskContext(batch=5)
input_data = json.loads(task_context.get_input_data())
img_id = input_data['id']
img_data = input_data['data']
img_data = np.asarray(img_data).astype('float32')
```
Each time we load the previously prepared input.json. Limits the number of loops to batches by decrementing batch by one for each load in `task_context.get_input_data()` function.

### To predict on input data
```python
y_keras = model.predict(img_data)
output_data = {}
output_data['key'] = img_id
output_data['data'] = y_keras.tolist()
task_context.set_output_data(json.dumps(output_data))
task_context = task_context.next()
```

Executes a loop as much as the batch size by returning instances decremented by 1 in `task_context.next()` function until batch becomes 0.
