import pprint 
import pandas as pd
import time
from IPython.display import display, FileLink, clear_output


def query_job_status( job_id,refresh_rate=3):
    pp = pprint.PrettyPrinter(indent=2)

    keep_running=True
    res=None
    while(keep_running):
        res = self.conn.get_exec(job_id)
        monitoring = pd.DataFrame(res.get_result(), index=[0])
        pd.set_option('max_colwidth', 120)
        clear_output()
        print("Refreshing every {} seconds".format(refresh_rate))
        display(monitoring)
        pp.pprint(res.get_result())
        if(res.get_result()['state'] not in ['PENDING_CRD_SCHEDULER', 'SUBMITTED','RUNNING']) :
            keep_running=False
        time.sleep(refresh_rate)
    return res

def update_model_profile_parameters(model_profile, 
                gpu_type, kernel_resource_group, kernel_consumer_path):
    model_profile['kernel']['gpu'] = gpu_type
    model_profile['resource_allocation']['kernel']['resource_group'] = kernel_resource_group
    model_profile['resource_allocation']['kernel']['consumer'] = kernel_consumer_path