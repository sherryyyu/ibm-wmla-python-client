#!/usr/bin/env python
import redhareapiversion
from redhareapi import Kernel
from wmla_client.extended_kernel import InferenceKernel



class Vgg19Kernel(InferenceKernel):

    def import_modules(self):
        import json
        import os
        import sys
        import numpy as np
        import tensorflow as tf
        import vgg19_network
        import vgg_preprocessing
        import time
        import base64

    def load_model(self, model_path, **kwargs):

        num_classes = kwargs.get("num_classes")
        label_file = kwargs.get("label_file")
        IMG_HEIGHT = kwargs.get("img_height")
        IMG_DEPTH = kwargs.get("img_depth")
        IMG_WIDTH = kwargs.get("img_width")

        #self.maximum_batchsize = MAXIMUM_BATCHSIZE
        image_filename_placeholder = tf.placeholder(tf.string)
        image_filecontent = tf.read_file(image_filename_placeholder)
        input_image = tf.image.decode_image(image_filecontent, channels=3)
        input_image = vgg_preprocessing.preprocess_image(self.input_image, IMG_HEIGHT, IMG_WIDTH, is_training=False)
        image_batch_placeholder = tf.placeholder(tf.float32, [None, IMG_HEIGHT, IMG_WIDTH, IMG_DEPTH])
        logits, _ = vgg19_network.vgg_19(image_batch_placeholder, num_classes,  is_training=False)
        net = tf.nn.softmax(logits)
        sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
        sess.run(tf.local_variables_initializer())
        saver = tf.train.Saver()

        ckpt = tf.train.get_checkpoint_state(model_path)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

        return {"net": net, "sess": sess, "ckpt": ckpt, "img_filename_holder": ;image_filename_placeholder, "img_filecontent": image_filecontent, "input_image": input_image, "image_batch_holder": image_batch_placeholder }


    def preprocces(self, data_list, attribute_list, model=None, **kwargs):
        processed_data = []
        sess = model.get("sess")
        input_image = model.get("input_image")
        image_filename_placeholder = model.get("img_filename_holder")
        image_filecontent = model.get("img_filecontent")

        data_attribute = zip(data_attribute)
        for data, attribute in data_attribute:
            if attribute.get("data_type") == 'image:jpeg_uri':
                img = sess.run(input_image, feed_dict={self.image_filename_placeholder: data})
                processed_data.append(img)

            elif attribute.get("data_type") == 'image:raw_data':
                image_content = base64.b64decode(data)
                img = sess.run(input_image, feed_dict={self.image_filecontent: image_content})
                processed_data.append(img)
            else:
                Vgg19Kernel.log_error("unsupport the data type:" + data_type)
        return processed_data


    def predict_func(self, model, batched_data, batched_attributes, **kwarsgs):
        batched_data = np.array(batched_data)
        pred = model.get("sess").run(model.get("net"), feed_dict={model.get("image_batch_older":batched_data})
        return pred

    def postprocess(self, predicted_results, attribute_list, **kwargs):

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

        file_name_list = [filename.get("filename") for filename in attribute_list]
        image_to_pred_dict=dict(zip(file_name_list, predicted_results))

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






        
            




      
    def on_task_invoke(self, task_context):
            prob_thresh = self.get_attribute(input_data['attributes'], 'threshold')
                if prob_thresh != ' ':
                    prob_thresh_vec.append(float(prob_thresh))
                else:
                    prob_thresh_vec.append(float(0.0))
        
            inputs = np.array(inputs)
            predictions = np.zeros((len(im_files_flat), self.num_classes), np.float32)
            start = time.time()
            for idx in range(0, len(im_files_flat), self.maximum_batchsize):
                batch_size = min(self.maximum_batchsize, len(im_files_flat) - idx)
                pred = self.sess.run(self.net, feed_dict={self.image_batch_placeholder:inputs[idx:idx+batch_size]})
                predictions[idx:idx+batch_size] = pred
                Vgg19Kernel.log_debug("%.2f%% finished in %.2f s." % (float(idx+batch_size)/len(im_files_flat)*100, (time.time()-start)))

            Vgg19Kernel.log_debug( "Done in %.2f s." % (time.time() - start))

           
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
