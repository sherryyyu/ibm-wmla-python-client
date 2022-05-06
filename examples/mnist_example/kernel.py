#!/usr/bin/env python
import redhareapiversion
from redhareapi import Kernel

import keras
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import decode_predictions
import numpy as np
import os, json, base64, time
import cv2

class MnistModel(Kernel):
    def on_kernel_start(self, kernel_context):
        try:
            Kernel.log_info("kernel input: " + kernel_context.get_model_description())
            model_desc = json.loads(kernel_context.get_model_description())
            model_path = model_desc['model_path']
            if model_path == '':
                model_path = os.getcwd()
            os.chdir(model_path)

            # Create Keras ResNet
            self.model = ResNet50(weights='imagenet')

            # Generate test samples
            self.img_shape = (224, 224, 3)
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
                img_data = base64.b64decode(input_data['data'])
                img = cv2.imdecode(np.fromstring(img_data, np.uint8), cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                Kernel.log_info("Image shape before resize: %s" % (img.shape,))
                # Naive resize, doesn't preserve aspect ratio
                img = cv2.resize(img, self.img_shape[:2], interpolation=cv2.INTER_AREA)
                y_keras = self.model.predict(np.reshape(img, (1,) + self.img_shape))
                tf_results = decode_predictions(y_keras, top=3)[0]
                output_data = {}
                output_data['key'] = img_id
                output_data['data'] = str(tf_results)
                task_context.set_output_data(json.dumps(output_data))
                task_context = task_context.next()
            end = time.time()
            Kernel.log_info("exit on_task_invoke, using time %.2f" % (end-start))
            Kernel.log_info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        except Exception as e:
            task_context.set_output_data(str(e))
            Kernel.log_error(str(e))

    def on_kernel_shutdown(self):
        Kernel.log_info('on_kernel_shutdown')

if __name__ == '__main__':
    obj_kernel = MnistModel()
    obj_kernel.run()