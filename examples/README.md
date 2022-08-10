# The explanation of kernel.py
The kernel run function consists of on_kernel_start(),on_task_invoke(),on_kernel_shutdown() in redhareapi.py. The first two functions should be implemented in kernel.py. The run function can make you load model and save output.

## on_kernel_start()
It should be run once when we start. In this function, you can load the model

### To load model
```python
kernel_context = KernelContext()
model_desc = json.loads(kernel_context.get_model_description())
model_path = model_desc['model_path']
model_path = model_path + '/' + model_desc['weight_path']
model = tf.keras.models.load_model(model_path)
```
We can get the model path from the model.json file which can be loaded by `KernelContext.get_model_description()`. If 'model_path' is not specified in model.json, the current working directory will be used as model_path by default. The model path is completed by appending 'model_path' to 'weight_path'. Then, we can load model from the model_path.

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
You can save output in this function, and this task is executed until the batch size is exhausted.

### To load input data
```python
task_context = TaskContext(batch=5)
input_data = json.loads(task_context.get_input_data())
img_id = input_data['id']
img_data = input_data['data']
img_data = np.asarray(img_data).astype('float32')
```
Each time we load the previously prepared input.json. Limits the number of loops to batches by decrementing batch by one for each load in `task_context.get_input_data()` function.

### To predict on input data and save output
```python
y_keras = model.predict(img_data)
output_data = {}
output_data['key'] = img_id
output_data['data'] = y_keras.tolist()
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


            
            model_desc = json.loads(kernel_context.get_model_description())
            model_path = model_desc['model_path']
            print('model_desc is',model_desc)
            print('model_path is',model_path)
            if model_path == '':
                model_path = os.getcwd()
            # os.chdir(model_path)
            Kernel.log_info("currect dir" + os.getcwd())

            model_path = model_path + '/' + model_desc['weight_path']

            # Create Keras ResNet
            self.model = tf.keras.models.load_model(model_path)

            # Generate test samples
            self.img_shape = (28, 28, 1)
            x_test = np.random.random_sample((1,) + self.img_shape)

            # Warm up
            y_keras = self.model.predict(x_test) # initialize the model first, don't take first predict into account
            start = time.time()
            y_keras = self.model.predict(x_test)
            end = time.time()
            Keras_time = end - start
            Kernel.log_info('Keras time : {0} s'.format(Keras_time))

        except Exception as e:
            Kernel.log_error(str(e))
            
    def on_task_invoke(self, task_context):
        try:
            start = time.time()
            Kernel.log_info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            Kernel.log_info('on_task_invoke')
            while task_context != None:
                input_data = json.loads(task_context.get_input_data())
                img_id = input_data['id']
                img_data = input_data['data']

                img_data = np.asarray(img_data).astype('float32')
                y_keras = self.model.predict(img_data)
                
                output_data = {}
                output_data['key'] = img_id
                output_data['data'] = y_keras.tolist()


                task_context.set_output_data(json.dumps(output_data))
                task_context = task_context.next()
            end = time.time()
            Kernel.log_info("exit on_task_invoke, using time %.2f" % (end-start))
            Kernel.log_info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        except Exception as e:
            task_context.set_output_data(str(e))
            Kernel.log_error(str(e))

if __name__ == '__main__':
    ppkernel = TestKernel()
    ppkernel.run()
```

## model.json
The weight path should be included in model.json to run kernel.py as follows:

```json
{
    "weight_path" : "mnist_model.h5",
}
```
