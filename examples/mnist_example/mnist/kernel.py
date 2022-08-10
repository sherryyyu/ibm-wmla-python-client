#!/usr/bin/env python

import redhareapiversion
from redhareapi import Kernel

import numpy as np
import os, json, base64, time
import tensorflow as tf

class MnistKernel(Kernel):
    def on_kernel_start(self, kernel_context):
        try:
            Kernel.log_info("kernel input: " + kernel_context.get_model_description())
            
            # load model.json
            model_desc = json.loads(kernel_context.get_model_description())
            model_path = model_desc['model_path']
            if model_path == '':
                model_path = os.getcwd()

            Kernel.log_info("currect dir" + os.getcwd())

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
    ppkernel = MnistKernel()
    ppkernel.run()
