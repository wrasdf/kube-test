import os
import importlib
from kubernetes import client, config
from kubernetes.client.rest import ApiException

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "config_manager.py")).load_module()
from config_manager import ConfigManager

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
class DeploymentManager:

    def __init__(self):
        ConfigManager()
        self.appApi = client.AppsV1Api()

    def list_namespaced_deployments(self, namespace):
        return list(map(lambda x: x.metadata.name, self.appApi.list_namespaced_deployment(namespace).items))

    def get_metadata(self, params):

        sidecarEnable = 'false'
        if 'sidecarEnable' in params:
            sidecarEnable = params['sidecarEnable']

        return client.V1ObjectMeta(
            name=params['name'],
            namespace=params['namespace'],
            labels={
                'app': params['name'],
                'purpose': 'test'
            },
            annotations={
                "sidecar.istio.io/inject": sidecarEnable
            }
        )

    def get_spec(self, params):
        return client.V1DeploymentSpec(
            replicas=params['replicas'],
            selector=client.V1LabelSelector(
                match_labels={
                    'app': params['name'],
                    'purpose': 'test'
                }
            ),
            strategy=client.V1DeploymentStrategy(
                type='RollingUpdate',
                rolling_update=client.V1RollingUpdateDeployment(
                    max_surge='50%',
                    max_unavailable=0
                )
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={
                        'app': params['name'],
                        'purpose': 'test'
                    }
                ),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name=params['name'],
                            image='{0}:{1}'.format(
                                params['container'], params['version']),
                            ports=[
                                client.V1ContainerPort(
                                    container_port=params['container_port'],
                                    name='http',
                                    protocol='TCP'
                                )
                            ],
                            liveness_probe=client.V1Probe(
                                http_get=client.V1HTTPGetAction(
                                    path='/api/v1/health',
                                    port=params['container_port']
                                ),
                                initial_delay_seconds=5,
                                period_seconds=5
                            ),
                            readiness_probe=client.V1Probe(
                                http_get=client.V1HTTPGetAction(
                                    path='/api/v1/health',
                                    port=params['container_port']
                                ),
                                initial_delay_seconds=5,
                                period_seconds=5
                            ),
                            resources=client.V1ResourceRequirements(
                                limits={
                                    'cpu': '250m',
                                    'memory': '1000Mi'
                                },
                                requests={
                                    'cpu': '100m',
                                    'memory': '128Mi'
                                }
                            )
                        )
                    ]
                )
            )
        )

    def create_namespaced_deployment(self, params):
        try:
            return self.appApi.create_namespaced_deployment(params['namespace'], client.V1Deployment(
                api_version='apps/v1',
                kind='Deployment',
                metadata=self.get_metadata(params),
                spec=self.get_spec(params)
            ))
        except ApiException as e:
            print("Exception when calling AppsV1Api -> create_namespaced_deployment: %s\n" % e)

    def patch_namespaced_deployment(self, params):
        try:
            return self.appApi.patch_namespaced_deployment(params['name'], params['namespace'], client.V1Deployment(
                api_version='apps/v1',
                kind='Deployment',
                metadata=self.get_metadata(params),
                spec=self.get_spec(params)
            ))
        except ApiException as e:
            print("Exception when calling AppsV1Api -> patch_namespaced_deployment: %s\n" % e)

    def apply_namespaced_deployment(self, params):
        if params['name'] in self.list_namespaced_deployments(params['namespace']):
            self.patch_namespaced_deployment(params)
        else:
            self.create_namespaced_deployment(params)

    def delete_namespaced_deployment(self, params):
        # No deployment
        if params['name'] not in self.list_namespaced_deployments(params['namespace']):
            print("No deployment resource {0} in namespace {1}".format(params['name'], params['namespace']))
            return True

        try:
            return self.appApi.delete_namespaced_deployment(params['name'], params['namespace'])
        except ApiException as e:
            print("Exception when calling AppsV1Api -> delete_namespaced_deployment: %s\n" % e)
