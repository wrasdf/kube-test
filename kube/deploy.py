import os
import importlib
from kubernetes import client, config
from kubernetes.client.rest import ApiException

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("config_manager", os.path.join(current_dir, "config_manager.py")).load_module()
from config_manager import ConfigManager

class DeployManager:

    def __init__(self):
        ConfigManager()
        self.api = client.AppsV1Api()

    # example of params:
    # {
    #     'name': 'test-deployment',
    #     'namespace': 'platform-enablement',
    #     'replicas': 2,
    #     'version: v0.1.6',
    #     'container': 'ikerry/metrics-node',
    #     'container_port': '8080',
    # }
    def create_deployment(self, params):

        defaultValue = {
            'name': 'test-deployment',
            'namespace': 'platform-enablement',
            'replicas': 1
        }
        results = dict(params, **defaultValue)
        metadata = client.V1ObjectMeta(
            name = results['name'],
            namespace = results['namespace'],
            labels = {
                'app': results['name'],
                'purpose': 'test'
            }
        )

        spec = client.V1DeploymentSpec(
            replicas = 1,
            selector = client.V1LabelSelector(
                match_labels = {
                    'app': results['name'],
                    'purpose': 'test'
                }
            ),
            strategy = client.V1DeploymentStrategy(
                type = 'RollingUpdate',
                rolling_update=client.V1RollingUpdateDeployment(
                    max_surge = '50%',
                    max_unavailable = 0
                )
            ),
            template = client.V1PodTemplateSpec(
                metadata = client.V1ObjectMeta(
                    labels = {
                        'app': results['name'],
                        'purpose': 'test'
                    }
                ),
                spec = client.V1PodSpec(
                    containers = [
                        client.V1Container(
                            name = results['name'],
                            image = '{0}:{1}'.format(results['container'], results['version']),
                            ports = [
                                client.V1ContainerPort(
                                    container_port = results['container_port'],
                                    name = 'http',
                                    protocol = 'TCP'
                                )
                            ],
                            liveness_probe = client.V1Probe(
                                http_get = client.V1HTTPGetAction(
                                    path = '/api/v1/health',
                                    port = results['container_port']
                                ),
                                initial_delay_seconds = 5,
                                period_seconds = 5
                            ),
                            readiness_probe = client.V1Probe(
                                http_get = client.V1HTTPGetAction(
                                    path = '/api/v1/health',
                                    port = results['container_port']
                                ),
                                initial_delay_seconds = 5,
                                period_seconds = 5
                            ),
                            resources = client.V1ResourceRequirements(
                                limits = {
                                    'cpu': '250m',
                                    'memory': '1000Mi'
                                },
                                requests = {
                                    'cpu': '100m',
                                    'memory': '128Mi'
                                }
                            )
                        )
                    ]
                )
            )
        )

        try:
            return self.api.create_namespaced_deployment(results['namespace'], client.V1Deployment(
                api_version = 'apps/v1',
                kind = 'Deployment',
                metadata = metadata,
                spec = spec
            ))
        except ApiException as e:
            print("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n" % e)

    def update_deployment(self, params):
        pass

    def create_ingress(self, params):
        pass

    def create_podDisruptionBudget(self, params):
        pass

    def create_service(self, params):
        pass


# de = DeployManager()
# de.create_deployment({
#     'name': 'test-deployment',
#     'namespace': 'platform-enablement',
#     'replicas': 2,
#     'version': 'v0.1.6',
#     'container': 'ikerry/metrics-node',
#     'container_port': 8080
# })

# TODO:
# - Common scenario test
#   - deploy kube-demo into current cluster
#   - test ingress works
#   - delete the app
# - kiam scenario test
#   - deploy kiam into current cluster
#   - test permission with s3 works
#   - delete the app
