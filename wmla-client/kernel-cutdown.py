#!/usr/bin/env python
import redhareapiversion
from redhareapi import Kernel

import json
import os
import sys


## Customer imports
import tensorflow as tf
import vgg19_network
import vgg_preprocessing
import numpy as np


import time
import base64


## Class import
class MiscKernel(Kernel):

    def postprocess(self, preds, **kwargs):
        response_output = preds
        return json.dumps(response_output)

    def attributes_to_dict(self, input_):
        return {att.get("key"):att.get("value") for att in input_.get("attributes")}

    def get_model(self, *args, **kwargs):
        #this is stateful so return true?
        pass

    def setup(self, *args, **kwargs):
        return output


    def load_model(self, *args, **kwargs):
        #this should return the loaded model

        return model

    def preprocces(self, input_data, **kwargs):

        processed_data = input_data

        return processed_data

    def do_inference(processed_data, model, **kwargs):
        preds = model.run(processed_data)

        return preds

    def on_kernel_start(self, kernel_context):
        try:
            self.model_details = json.loads(kernel_context.get_model_description())


            MiscKernel.log_info("on_kernel_start")
            MiscKernel.log_info("mc instance id: " + kernel_context.get_instance_id())
            MiscKernel.log_info("mc input content: " + kernel_context.get_model_description())
            MiscKernel.log_info("Loading Inference Model..")
            MiscKernel.log_info("model_desc" + str(model_desc))

            model_path = model_desc['model_path']
            if model == ' ':
                raise IOError(('error: Model not found.\n'))

            attribute_dict = self.attributes_to_dict(model_desc)

            model = self.get_model(self, model_path, **attribute_dict)
            self.model = self.load_model(self, *model)

            ## Need to output some specifics here
            MiscKernel.log_info("ckpt:" + str(ckpt) +', model:' + model)

            MiscKernel.log_info('loaded network:' + model)

        except Exception as e:
            MiscKernel.log_error("-------------------------")
            MiscKernel.log_error(str(e))
            task_context.set_output_data("Failed due to:" + str(e))
            MiscKernel.log_error("-------------------------")

    def on_task_invoke(self, task_context):
        try:

            outputs = self.setup()

            # Setup batch lists

            while task_context != None:
                MiscKernel.log_debug("on_task_invoke")
                MiscKernel.log_debug("version: " + str(task_context.get_version()))
                MiscKernel.log_debug("model name: " + task_context.get_model_name())
                MiscKernel.log_debug("task id: " + task_context.get_id())
                MiscKernel.log_debug("session id: " + task_context.get_session_id())
                MiscKernel.log_debug("input data: " + task_context.get_input_data())

                # Load input data
                input_data = json.loads(task_context.get_input_data())
                attribute_dict = self.attributes_to_dict(input_data)

                ## Convert attributes to lists or not incase its not batch
                MiscKernel.log_debug("prob_thresh_vec" + str(prob_thresh_vec))
                data_type = input_data['data_type']
                MiscKernel.log_info("data_type: " + data_type)

                # Handle different data types and prep lists for processing
                if data_type == 'image:jpeg_uri':
                    im_files = [os.path.basename(x['value']) for x in input_data['data_value']]
                    im_files_vec.append(im_files)
                    im_files_flat += im_files
                    im_data_value_flat += [x['value'] for x in input_data['data_value']]
                elif data_type == 'image:raw_data':
                    im_files = [x['key'] for x in input_data['data_value']]
                    im_files_vec.append(im_files)
                    im_files_flat += im_files
                    im_data_value_flat += [x['value'] for x in input_data['data_value']]
                else:
                    MiscKernel.log_error("unsupport the data type:" + data_type)


                MiscKernel.log_debug("call next")
                task_context_vec.append(task_context)
                task_context = task_context.next()
                MiscKernel.log_debug("next context: " + str(task_context))

            inputs = []

            ## Pre-process data into the correct format - need exception where the format does not align


            start = time.time()

            ## Loop through the dataset to do predictions
            MiscKernel.log_debug("%.2f%% finished in %.2f s." % (float(idx+batch_size)/len(im_files_flat)*100, (time.time()-start)))

            MiscKernel.log_debug( "Done in %.2f s." % (time.time() - start))


            ## Convert to outputs in the correct format

            MiscKernel.log_debug("return ret "+str(index)+", im_files "+str(im_files)+", ctx "+str(task_context))

            task_context.set_output_data(ret)

        except Exception as e:
            MiscKernel.log_error("-------------------------")
            MiscKernel.log_error( str(e) )
            task_context.set_output_data("Failed due to: " + str(e))
            MiscKernel.log_error("-------------------------")

    def on_kernel_shutdown(self):
        MiscKernel.log_info( 'on_kernel_shutdown')

if __name__ == '__main__':
    obj_kernel = MiscKernel()
    obj_kernel.run()

