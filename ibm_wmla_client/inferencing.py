from ibm_wmla import DeepLearningImpactV1
from ibm_wmla import ElasticDistributedInferenceV2
import os
import tempfile
import shutil
from distutils.dir_util import copy_tree



ARGS_V1 = ""
ARGS_V2 = ""

class Inference(object):
    def __init__(self, connection, model_name):
        self.conn = connection.service_edi
        self.model_name = model_name
    
    def get_model_details(self):
        model_details = self.conn.get_model(self.model_name).result() 
        model_profile = self.conn.get_model_profile(self.model_name).result() 
        return model_details, model_profile

    def get_model_deployed(self):
        ## lift models first and g check lift
        deployed_model_list = self.conn.get_models().result() 
        if self.model_name in deployed_model_list:
            return True
        else:
            return False   

    def _copyfiles(self, paths):
        temp_path = tempfile.mkdtemp()
        for path in list_paths:
            if os.path.isfile(path):
          	    try:
            	    shutil.copy(path, temp_path )
         	    except:
                    print("Failed to copy file")
                    break
            elif os.path.isdir(path):
                try: 
                    copy_tree(path, temp_path)
                except:
                    print("Failed to copy directory")
            else:
                print("Not a file or directory")

    def _generate_files(self, objects):
        
        


    def deploy(self, kernel, model_json, readme, paths):
        if isinstance(kernel, String) or isinstance(kernel, os.Path):
            self._copyfiles()
        elif:
            generate_files
            
            copyfiles
        else:
            error

        tar_files
        if not get_model_deployed():
            try: 
                deploy_responce = sdk.deploy(self.model_name, files)
            except:
                print("failed")
        else:
             print("model deployed please refrlppy instead")

    def start(self):
        if self.get_model_deployed():
            service_edi.start(self.model_name))
        else:
            print("no model named ___ deployed")

    def stop(self):

        
        # step one is create the tar
        #step two is Deploy



    def configure(self, framework=None, gpus_per_worker, num_workers):

        pickle.save("/tmp/model_func.pickle", model_train_func)

        args =


        pas

    def create_model_json(self):
        pass

    def create_kernel(self, get_model_files_func, load_model_func, pre
    process_input_func, inference_func, responce_output_func, clean_up_func):
        # Need a template class that inserts specifics into the kernel.py file


        pass

    def

    def _create_tar(self):




    def dist_train(self):
        pass

    def elastic_dist_train(self):
        pass

    def hpo(self):
        pass

