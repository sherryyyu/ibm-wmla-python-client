from ibm_wmla import DeepLearningImpactResTfulApIsV1
from ibm_wmla import DeepLearningImpactResTfulApIsV2
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator
from ibm_cloud_sdk_core.authenticators import BearerTokenAuthenticator


class Connection(object):

    def __init__(self, service_url, service_instance, wmla_v1=False,
                 apikey=None, username=None, password=None):
        self.url = service_url
        self.instance = service_instance
        self.apikey = apikey
        self.user = username
        self.password = password
        self.legacy = wmla_v1

    def connect(self):
        if self.legacy:
            # create the authenticator
            authenticator = BasicAuthenticator(self.user, self.password)
            self.service = DeepLearningImpactResTfulApIsV1(
                    authenticator=authenticator)
            self.service.configure_service(self.instance)
            self.service.set_service_url(self.url)
        elif self.apikey:
            # in the constructor, assuming control of managing the token
            authenticator = BearerTokenAuthenticator(self.apikey)
            self.service = DeepLearningImpactResTfulApIsV2(
                    authenticator=authenticator)
            self.service.configure_service(self.instance)
            self.service.set_service_url(self.url)
        else:
            authenticator = BasicAuthenticator(self.user, self.password)
            self.service = DeepLearningImpactResTfulApIsV2(
                    authenticator=authenticator)
            self.service.configure_service(self.instance)
            self.service.set_service_url(self.url)










