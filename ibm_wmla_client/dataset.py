from ibm_wmla import DeepLearningImpactResTfulApIsV1
from ibm_wmla import DeepLearningImpactResTfulApIsV2
import os
import tempfile
import shutil
import json
from distutils.dir_util import copy_tree
import dill
import utils
import wmla_client


class Dataset(object):
    def __init__(self, connection, sig_name, data_dir):
        self.conn = connection.service
        self.sig_name = sig_name
        self.data_dir = data_dir         

    def download(self, func, poll_logs=False, **kwargs):
        temp_path = tempfile.mkdtemp()

        with open(temp_path + "/params.json", "w") as f:
            json.dump(kwargs, f)

        if isinstance(func, str):
            shutil.copy(func, temp_path + "/download.py")
        
        else:
            with open(temp_path + "/func.pickle", "wb") as f: 
                dill.dump(func, f)

        wmla_asset_path = wmla_client.__file__ + "/assets/download.py"
        shutil.copy(wmla_asset_path, temp_path )

        ##TODO ensure we dont use a GPU for this step
        args_command = "--exec-start PyTorch --model-main download.py --data_dir %s" % (self.data_dir)

        try: 
            response = self.conn.create_exec(self.sig_name, args_command, temp_path + "/download.modelDir.tar" )

            if not response.ok:
                print('submit job failed: code=%s, %s'%(response.status_code, response.get_result()))

            else:
                if poll_logs:
                    utils.query_job_status(response.get_results().get("ID"))
        except:
            print("Failed to submit request")


        return response.get_result()

    

        







        

        

        

        

        ## dill func to file 
        ## write standard main.py 

        

        # Write func to file 
        # Turn args into json dict
        # package up and submitt to cluster 
        # Get logs 


        


    






