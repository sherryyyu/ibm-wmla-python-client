# from ibm_wmla.wmla_api_v1 import DeepLearningImpactV1
from ibm_wmla.wmla_api_edi_v2 import ElasticDistributedInferenceV2
from ibm_wmla.edi_authentication import ElasticDistributedInferenceAuthenticator
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator
from ibm_cloud_sdk_core.authenticators import BearerTokenAuthenticator


class Connection(object):

    def __init__(self, service_url, service_instance, wmla_v1=False, edi=False, 
                 apikey=None, username=None, password=None, user_access_token = None):
        self.url = service_url
        self.instance = service_instance
        self.apikey = apikey
        self.user = username
        self.password = password
        self.user_access_token = user_access_token
        self.legacy = wmla_v1
        self.edi = edi

    def connect(self):
        if self.legacy:
            if not self.edi:
                print("Connecting to DLI")
                # create the authenticator
                authenticator = BasicAuthenticator(self.user, self.password)
                self.service_dli = DeepLearningImpactV1(
                        authenticator=authenticator)
                self.service_dli.configure_service(self.instance)
                self.service_dli.set_service_url(self.url)
            else:
                print("Connecting to EDI")
                edi_authenticator = ElasticDistributedInferenceAuthenticator(self.user, self.password, self.user_access_token, self.url, disable_ssl_verification = True)
                print("EDI Token created")
                self.service_edi = ElasticDistributedInferenceV2(
                        authenticator=edi_authenticator)
                self.service_edi.configure_service(self.instance)
                self.service_edi.set_service_url(self.url)

                print("EDI Service connected")
        elif self.apikey:
            # in the constructor, assuming control of managing the token
            authenticator = BearerTokenAuthenticator(self.apikey)
            self.service = DeepLearningImpactV1(
                    authenticator=authenticator)
            self.service.configure_service(self.instance)
            self.service.set_service_url(self.url)
        else:
            authenticator = BasicAuthenticator(self.user, self.password)
            self.service = DeepLearningImpactV1(
                    authenticator=authenticator)
            self.service.configure_service(self.instance)
            self.service.set_service_url(self.url)










