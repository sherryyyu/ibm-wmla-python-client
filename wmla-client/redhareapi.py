###############################################################################
# Licensed Materials - Property of IBM
# 5725-Y38
# @ Copyright IBM Corp. 2018-2020 All Rights Reserved
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
###############################################################################

import os
import json
import datetime
import traceback

LEVEL = {
            -1: "D",
             0: "I",
             1: "W",
             2: "E"
        }

class KernelContext(object):

    def get_id(self):
        return "local"

    def get_model_description(self):
        #just read the model.json
        with open("./model.json",'r') as load_f:
            model_desc = json.load(load_f)
            if 'model_path' not in model_desc:
                model_desc['model_path'] = os.getcwd()

        return json.dumps(model_desc)


class TaskContext(object):

    def __init__(self, batch=4):
        self.batch_size = batch
    
    def get_id(self):
        return "local"

    def get_uuid(self):
        return "local"

    def get_session_id(self):
        return "local"

    def get_job_id(self):
        return "local"

    def get_input_data(self):
        if self.batch_size:
            self.batch_size -= 1

        #just read the input.json
        with open("./input.json",'r') as load_f:
            return load_f.read()

    def get_input_data_extend(self):
        return self.get_input_data()

    def set_output_data(self, data):
        print("Response data: {}".format(data))
        return True

    def set_output_data_extend(self, data):
        print(data)
        return True

    def report_ready(self, data):
        return True

    def next(self):
        if self.batch_size:
            return self

    def prev(self):
        return None

class Kernel(object):

    def on_kernel_start(self, kernel_context):
        return

    def on_task_invoke(self, task_context):
        return

    def on_kernel_shutdown(self):
        return

    def run(self):
       self.on_kernel_start(KernelContext())
       self.on_task_invoke(TaskContext(5))
       self.on_kernel_shutdown()

    @staticmethod
    def log(level, msg):
        print("{}: {} {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), LEVEL[level], msg))

    @staticmethod
    def log_debug(msg):
        Kernel.log(-1, msg)

    @staticmethod
    def log_info(msg):
        Kernel.log(0, msg)

    @staticmethod
    def log_warn(msg):
        Kernel.log(1, msg)

    @staticmethod
    def log_error(msg):
        Kernel.log(2, msg)

