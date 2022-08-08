#!/usr/bin/env python

import redhareapiversion
from redhareapi import Kernel

import numpy as np
import os, json, base64, time
import tensorflow as tf

class TestKernel(Kernel):
    def on_kernel_start(self, kernel_context):
        try:
            Kernel.log_info("kernel input: " + kernel_context.get_model_description())
            
            model_desc = json.loads(kernel_context.get_model_description())
            model_path = model_desc['model_path']
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
