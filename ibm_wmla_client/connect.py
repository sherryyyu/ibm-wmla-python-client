from ibm_wmla import DeepLearningImpactV1
from ibm_wmla import ElasticDistributedInferenceV2
from ibm_wmla import
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator
from ibm_cloud_sdk_core.authenticators import BearerTokenAuthenticator


class Connection(object):

    def __init__(self, service_url, service_instance, wmla_v1=False, edi=False, 
                 apikey=None, username=None, password=None, edi_url=None):
        self.url = service_url
        self.instance = service_instance
        self.apikey = apikey
        self.user = username
        self.password = password
        self.legacy = wmla_v1
        self.edi = edi
        self.edi_url = edi_url

    def connect(self):
        if self.legacy:
            # create the authenticator
            authenticator = BasicAuthenticator(self.user, self.password)
            self.service_dli = DeepLearningImpactV1(
                    authenticator=authenticator)
            self.service_dli.configure_service(self.instance)
            self.service_dli.set_service_url(self.url)
            if self.edi:
                edi_authenticator = ElasticDistributedInferenceAuthenticator(self.user, self.password, self.edi_url)
                self.service_edi = ElasticDistributedInferenceV2(
                        authenticator=edi_authenticator)
                self.service_edi.configure_service(self.instance)
                self.service_edi.set_service_url(self.edi_url)
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










