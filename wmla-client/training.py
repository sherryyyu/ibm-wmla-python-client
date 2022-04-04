from ibm_wmla import DeepLearningImpactResTfulApIsV1
from ibm_wmla import DeepLearningImpactResTfulApIsV2
import os
import tempfile
import shutil
from distutils.dir_util import copy_tree



ARGS_V1 = ""
ARGS_V2 = ""

class Training(object):
    def __init__(self, connection, sig_name, dataset, framework):
        self.conn = connection.service
        self.sig_name = sig_name
        self.framework = framework
        self.dataset = dataset

    def start(self):
        pass



    def configure(self, framework=None, gpus_per_worker, num_workers):

        pickle.save("/tmp/model_func.pickle", model_train_func)

        args =


        pas


class Training(object):
    def __init__(self, connection):
        self.conn = connection

    def train(self, model_train_func, framework=None, gpus_per_worker, num_workers):
        
        pickle.save("/tmp/model_func.pickle", model_train_func)
        
        args = 


        pas
        
    def _find_modules(self, func):
        
    def _find_module_path(self, module):
        module.__file__ ## should provide the path 
        os.path.dirname(__file__) ## returns abs path 
        
    
    def _create_tar(self):
    
    
    

    def dist_train(self):
        pass

    def elastic_dist_train(self):
        pass

    def hpo(self):
        pass




    # List VPCs
    print("List Templates for the Frameworks")
    try:
        templates = service. get_model_template_details(framework="tensorflow")
        print(templates)
    except ApiException as e:
        print("List Power Cloud failed with status code " + str(e.code) + ": " + e.message)
