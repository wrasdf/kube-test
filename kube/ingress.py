import os
import importlib
from kubernetes import client, config
from kubernetes.client.rest import ApiException

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "config_manager.py")).load_module()
importlib.machinery.SourceFileLoader("secret", os.path.join(current_dir, "secret.py")).load_module()
from config_manager import ConfigManager
from secret import SecretManager

# example of params:
# {
#     'name': 'test-deployment',
#     'namespace': 'platform-enablement',
#     'replicas': 2,
#     'version: v0.1.6',
#     'container': 'ikerry/metrics-node',
#     'container_port': '8080',
#     'dns_name': 'nodet.svc.platform.myobdev.com',
# }
class IngressManager:

    def __init__(self):
        ConfigManager()
        self.extensionApi = client.ExtensionsV1beta1Api()

    def list_namespaced_ingress(self, namespace):
        return list(map(lambda x: x.metadata.name, self.extensionApi.list_namespaced_ingress(namespace).items))

    def get_metadata(self, params):
        return client.V1ObjectMeta(
            name=params['name'],
            namespace=params['namespace'],
            labels={
                'app': params['name'],
                'purpose': 'test'
            },
            annotations={
                "kubernetes.io/tls-acme": "true"
            }
        )

    def get_spec(self, params):
        return client.ExtensionsV1beta1IngressSpec(
            tls=[
                client.ExtensionsV1beta1IngressTLS(
                    hosts=[
                        params['dns_name']
                    ],
                    secret_name='{0}-tls'.format(params['name'])
                )
            ],
            rules=[
                client.ExtensionsV1beta1IngressRule(
                    host=params['dns_name'],
                    http=client.ExtensionsV1beta1HTTPIngressRuleValue(
                        paths=[
                            client.ExtensionsV1beta1HTTPIngressPath(
                                path='/',
                                backend=client.ExtensionsV1beta1IngressBackend(
                                    service_name=params['name'],
                                    service_port=params['container_port']
                                )
                            )
                        ]
                    )
                )
            ]
        )

    def create_namespaced_ingress(self, params):
        try:
            return self.extensionApi.create_namespaced_ingress(
                params['namespace'],
                client.ExtensionsV1beta1Ingress(
                    api_version='extensions/v1beta1',
                    kind='Ingress',
                    metadata=self.get_metadata(params),
                    spec=self.get_spec(params)
                )
            )
        except ApiException as e:
            print(
                "Exception when calling ExtensionsV1beta1Api->create_namespaced_ingress: %s\n" % e)

    def patch_namespaced_ingress(self, params):
        try:
            return self.extensionApi.patch_namespaced_ingress(
                params['name'],
                params['namespace'],
                client.ExtensionsV1beta1Ingress(
                    api_version='extensions/v1beta1',
                    kind='Ingress',
                    metadata=self.get_metadata(params),
                    spec=self.get_spec(params)
                )
            )
        except ApiException as e:
            print(
                "Exception when calling ExtensionsV1beta1Api->patch_namespaced_ingress: %s\n" % e)

    def apply_namespaced_ingress(self, params):
        if params['name'] in self.list_namespaced_ingress(params['namespace']):
            self.patch_namespaced_ingress(params)
        else:
            self.create_namespaced_ingress(params)

    def delete_namespaced_ingress(self, params):
        # No ingress
        if params['name'] not in self.list_namespaced_ingress(params['namespace']):
            print("No ingress resource {0} in namespace {1}".format(params['name'], params['namespace']))
            return True

        try:
            self.extensionApi.delete_namespaced_ingress(
                params['name'],
                params['namespace']
            )
        except ApiException as e:
            print(
                "Exception when calling ExtensionsV1beta1Api->delete_namespaced_ingress: %s\n" % e)
