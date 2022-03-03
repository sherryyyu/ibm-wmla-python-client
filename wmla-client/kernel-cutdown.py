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

    def attributes_to_dict(self):
        return {att.get("key"):att.get("value") for att in self.model_details.get("attributes")}

    def get_model(self, *args, **kwargs):
        #this is stateful so return true?
        pass


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
            MiscKernel.log_info("loading vgg19 inference model..")
            MiscKernel.log_info("model_desc" + str(model_desc))


            model_path = model_desc['model_path']
            if model == ' ':
                raise IOError(('error: Model not found.\n'))


            attribute_dict = self.attributes_to_dict()


            self.image_filename_placeholder = tf.placeholder(tf.string)
            self.image_filecontent = tf.read_file(self.image_filename_placeholder)
            self.input_image = tf.image.decode_image(self.image_filecontent, channels=3)
            self.input_image = vgg_preprocessing.preprocess_image(self.input_image, IMG_HEIGHT, IMG_WIDTH, is_training=False)
            self.image_batch_placeholder = tf.placeholder(tf.float32, [None, IMG_HEIGHT, IMG_WIDTH, IMG_DEPTH])
            logits, _ = vgg19_network.vgg_19(self.image_batch_placeholder, NUM_CLASSES,  is_training=False)
            self.net = tf.nn.softmax(logits)
            self.sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
            self.sess.run(tf.local_variables_initializer())
            saver = tf.train.Saver()

            ckpt = tf.train.get_checkpoint_state(model)
            MiscKernel.log_info("ckpt:" + str(ckpt) +', model:' + model)
            if ckpt and ckpt.model_checkpoint_path:
                MiscKernel.log_info("restoring checkpoint")
                saver.restore(self.sess, ckpt.model_checkpoint_path)

            MiscKernel.log_info('loaded network:' + model)

        except Exception as e:
            MiscKernel.log_error("-------------------------")
            MiscKernel.log_error(str(e))
            task_context.set_output_data("Failed due to:" + str(e))
            MiscKernel.log_error("-------------------------")

    def on_task_invoke(self, task_context):
        try:
            task_context_vec=[]
            im_files_vec=[]
            im_files_flat=[]
            im_data_value_flat=[]
            prob_thresh_vec=[]

            while task_context != None:
                MiscKernel.log_debug("on_task_invoke")
                MiscKernel.log_debug("version: " + str(task_context.get_version()))
                MiscKernel.log_debug("model name: " + task_context.get_model_name())
                MiscKernel.log_debug("task id: " + task_context.get_id())
                MiscKernel.log_debug("session id: " + task_context.get_session_id())
                MiscKernel.log_debug("input data: " + task_context.get_input_data())

                input_data = json.loads(task_context.get_input_data())
                prob_thresh = self.get_attribute(input_data['attributes'], 'threshold')
                if prob_thresh != ' ':
                    prob_thresh_vec.append(float(prob_thresh))
                else:
                    prob_thresh_vec.append(float(0.0))
                MiscKernel.log_debug("prob_thresh_vec" + str(prob_thresh_vec))
                data_type = input_data['data_type']
                MiscKernel.log_info("data_type: " + data_type)
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

            if data_type == 'image:jpeg_uri':
                for image_filename in im_data_value_flat:
                    img = self.sess.run(self.input_image, feed_dict={self.image_filename_placeholder: image_filename})
                    inputs.append(img)

            elif data_type == 'image:raw_data':
                for image_file in im_data_value_flat:
                    MiscKernel.log_debug("base64 start decode str len"+ str(len(image_file)))
                    image_content = base64.b64decode(image_file)
                    MiscKernel.log_debug("base64 end decode")
                    img = self.sess.run(self.input_image, feed_dict={self.image_filecontent: image_content})
                    MiscKernel.log_debug("processed image with shape "+str(img.shape))
                    inputs.append(img)
            else:
                MiscKernel.log_error("unsupport the data type:" + data_type)

            inputs = np.array(inputs)
            predictions = np.zeros((len(im_files_flat), self.num_classes), np.float32)
            start = time.time()
            for idx in range(0, len(im_files_flat), self.maximum_batchsize):
                batch_size = min(self.maximum_batchsize, len(im_files_flat) - idx)
                pred = self.sess.run(self.net, feed_dict={self.image_batch_placeholder:inputs[idx:idx+batch_size]})
                predictions[idx:idx+batch_size] = pred
                MiscKernel.log_debug("%.2f%% finished in %.2f s." % (float(idx+batch_size)/len(im_files_flat)*100, (time.time()-start)))

            MiscKernel.log_debug( "Done in %.2f s." % (time.time() - start))

            image_to_pred_dict=dict(zip(im_files_flat, predictions))

            for index in range(len(task_context_vec)):
                task_context=task_context_vec[index]
                im_files=im_files_vec[index]
                MiscKernel.log_debug("return ret "+str(index)+", im_files "+str(im_files)+", ctx "+str(task_context))
                task_imagename=[]
                task_predictions=[]
                for imagename in im_files:
                    pred = image_to_pred_dict[imagename]
                    task_imagename.append(imagename)
                    task_predictions.append(pred)

                prob_thresh = prob_thresh_vec[index]
                ret=self.getClassifyInferenceResult(task_imagename, task_predictions, prob_thresh=prob_thresh, label_file=self.label_file)
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

