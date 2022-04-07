from ibm_wmla import DeepLearningImpactResTfulApIsV1
from ibm_wmla import DeepLearningImpactResTfulApIsV2
import os
import tempfile
import shutil
from distutils.dir_util import copy_tree



ARGS_V1 = ""
ARGS_V2 = ""

class Training(object):
    def __init__(self, connection, sig_name, dataset, result_dir, framework):
        self.conn = connection.service
        self.sig_name = sig_name
        self.framework = framework
        self.dataset = dataset
        self.result_dir = result_dir


    def train(self, func, libs_path = None, poll_logs=False, **kwargs):
        temp_path = tempfile.mkdtemp()

        with open(temp_path + "/params.json", "w") as f:
            json.dump(kwargs, f)

        if libs_path:
            copy_tree(libs_path, temp_path)

        if isinstance(func, str):
            shutil.copy(func, temp_path + "/train.py")

        else:
            with open(temp_path + "/func.pickle", "wb") as f: 
                dill.dump(func, f)
            
            wmla_asset_path = wmla_client.__file__ + "/assets/train.py"
            shutil.copy(wmla_asset_path, temp_path )

        ##TODO ensure we dont use a GPU for this step
        args_command = "--exec-start %s --model-main train.py --data_dir %s --result_dir %s" % (framework, self.dataset.data_dir, self.result_dir)

        try: 
            response = self.conn.create_exec(self.sig_name, args_command, temp_path + "/train.modelDir.tar" )

            if not response.ok:
                print('submit job failed: code=%s, %s'%(response.status_code, response.get_result()))

            else:
                if poll_logs:
                    utils.query_job_status(response.get_results().get("ID"))
        except:
            print("Failed to submit request")


        return response.get_result()






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
