from ibm_wmla import DeepLearningImpactResTfulApIsV1
from ibm_wmla import DeepLearningImpactResTfulApIsV2

class Training(object):
    def __init__(self, connection):
        self.conn = connection

    def train(self, model_train_func):


        pass

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
