#!/usr/bin/env python
import redhareapiversion
from redhareapi import Kernel

import json
import os
import sys
import numpy as np
import tensorflow as tf
import vgg19_network
import vgg_preprocessing
import time
import base64


class Vgg19Kernel(Kernel):
    def _getLabel(self, id, labels = None):
        id = int(id)
        if labels and len(labels) > id:
            return labels[id]
        return str(id)

    def getClassifyInferenceResult(self, sample_id, prediction, prob_thresh = 0.0, label_file = None):
        if label_file and os.path.exists(label_file):
            CLASSES = [line.strip() for line in open(label_file) if line]
        else:
            CLASSES = None
        output_dict = {"type":"classification", "result":[]}

        for i in np.arange(len(prediction)):
            sampleId = os.path.basename(sample_id[i])
            pred = prediction[i]
            top_k = pred.flatten().argsort()[::-1]
            j = 0
            go = True
            while go:
                if (j < len(top_k) and pred[top_k[j]] >= prob_thresh):
                    label = self._getLabel(top_k[j], CLASSES)
                    prob = float('%.3f'%pred[top_k[j]])
                    output_dict['result'].append({"sampleId":sampleId, "label":label, "prob":prob})
                    j+=1
                else:
                    go = False

        return json.dumps(output_dict)

    def get_attribute(self, attributes, attribute_name):
        value = None
        for attribute in attributes:
            Vgg19Kernel.log_debug("get " + attribute_name + " from attribute: "+ str(attribute) )
            if attribute['key'] == attribute_name:
                value = attribute['value']
                break
        return value
    def on_kernel_start(self, kernel_context):
        try:
            Vgg19Kernel.log_info("on_kernel_start")
            Vgg19Kernel.log_info("mc instance id: " + kernel_context.get_instance_id())
            Vgg19Kernel.log_info("mc input content: " + kernel_context.get_model_description())
            model_desc = json.loads(kernel_context.get_model_description())
            Vgg19Kernel.log_info("loading vgg19 inference model..")
            Vgg19Kernel.log_info("model_desc" + str(model_desc))
            model = model_desc['model_path']
            if model == ' ':
                raise IOError(('error: Model not found.\n'))

            IMG_HEIGHT =  int(self.get_attribute(model_desc['attributes'], 'img_height'))
            IMG_WIDTH = int(self.get_attribute(model_desc['attributes'], 'img_width'))
            IMG_DEPTH = int(self.get_attribute(model_desc['attributes'], 'img_depth'))
            MAXIMUM_BATCHSIZE = int(self.get_attribute(model_desc['attributes'], 'maximum_batchsize'))
            NUM_CLASSES =  int(self.get_attribute(model_desc['attributes'],'num_classes'))

            self.num_classes = NUM_CLASSES

            self.label_file = None
            lableFlie=self.get_attribute(model_desc['attributes'],'label_file')
            if lableFlie != None:
                self.label_file = lableFlie
            self.maximum_batchsize = MAXIMUM_BATCHSIZE
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
            Vgg19Kernel.log_info("ckpt:" + str(ckpt) +', model:' + model)
            if ckpt and ckpt.model_checkpoint_path:
                Vgg19Kernel.log_info("restoring checkpoint")
                saver.restore(self.sess, ckpt.model_checkpoint_path)

            Vgg19Kernel.log_info('loaded network:' + model)

        except Exception as e:
            Vgg19Kernel.log_error("-------------------------")
            Vgg19Kernel.log_error(str(e))
            task_context.set_output_data("Failed due to:" + str(e))
            Vgg19Kernel.log_error("-------------------------")

    def on_task_invoke(self, task_context):
        try:
            task_context_vec=[]
            im_files_vec=[]
            im_files_flat=[]
            im_data_value_flat=[]
            prob_thresh_vec=[]

            while task_context != None:
                Vgg19Kernel.log_debug("on_task_invoke")
                Vgg19Kernel.log_debug("version: " + str(task_context.get_version()))
                Vgg19Kernel.log_debug("model name: " + task_context.get_model_name())
                Vgg19Kernel.log_debug("task id: " + task_context.get_id())
                Vgg19Kernel.log_debug("session id: " + task_context.get_session_id())
                Vgg19Kernel.log_debug("input data: " + task_context.get_input_data())

                input_data = json.loads(task_context.get_input_data())
                prob_thresh = self.get_attribute(input_data['attributes'], 'threshold')
                if prob_thresh != ' ':
                    prob_thresh_vec.append(float(prob_thresh))
                else:
                    prob_thresh_vec.append(float(0.0))
                Vgg19Kernel.log_debug("prob_thresh_vec" + str(prob_thresh_vec))
                data_type = input_data['data_type']
                Vgg19Kernel.log_info("data_type: " + data_type)
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
                    Vgg19Kernel.log_error("unsupport the data type:" + data_type)
                Vgg19Kernel.log_debug("call next")
                task_context_vec.append(task_context)
                task_context = task_context.next()
                Vgg19Kernel.log_debug("next context: " + str(task_context))

            inputs = []

            if data_type == 'image:jpeg_uri':
                for image_filename in im_data_value_flat:
                    img = self.sess.run(self.input_image, feed_dict={self.image_filename_placeholder: image_filename})
                    inputs.append(img)

            elif data_type == 'image:raw_data':
                for image_file in im_data_value_flat:
                    Vgg19Kernel.log_debug("base64 start decode str len"+ str(len(image_file)))
                    image_content = base64.b64decode(image_file)
                    Vgg19Kernel.log_debug("base64 end decode")
                    img = self.sess.run(self.input_image, feed_dict={self.image_filecontent: image_content})
                    Vgg19Kernel.log_debug("processed image with shape "+str(img.shape))
                    inputs.append(img)
            else:
                Vgg19Kernel.log_error("unsupport the data type:" + data_type)

            inputs = np.array(inputs)
            predictions = np.zeros((len(im_files_flat), self.num_classes), np.float32)
            start = time.time()
            for idx in range(0, len(im_files_flat), self.maximum_batchsize):
                batch_size = min(self.maximum_batchsize, len(im_files_flat) - idx)
                pred = self.sess.run(self.net, feed_dict={self.image_batch_placeholder:inputs[idx:idx+batch_size]})
                predictions[idx:idx+batch_size] = pred
                Vgg19Kernel.log_debug("%.2f%% finished in %.2f s." % (float(idx+batch_size)/len(im_files_flat)*100, (time.time()-start)))

            Vgg19Kernel.log_debug( "Done in %.2f s." % (time.time() - start))

            image_to_pred_dict=dict(zip(im_files_flat, predictions))

            for index in range(len(task_context_vec)):
                task_context=task_context_vec[index]
                im_files=im_files_vec[index]
                Vgg19Kernel.log_debug("return ret "+str(index)+", im_files "+str(im_files)+", ctx "+str(task_context))
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
            Vgg19Kernel.log_error("-------------------------")
            Vgg19Kernel.log_error( str(e) )
            task_context.set_output_data("Failed due to: " + str(e))
            Vgg19Kernel.log_error("-------------------------")

    def on_kernel_shutdown(self):
        Vgg19Kernel.log_info( 'on_kernel_shutdown')

if __name__ == '__main__':
    obj_kernel = Vgg19Kernel()
    obj_kernel.run()

