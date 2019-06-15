import unittest
from kube.ingress import IngressManager
from kube.deployment import DeploymentManager
from kube.service import ServiceManager

class TestNamespaceManager(unittest.TestCase):

    def setUp(self):
        self.deployment_manager = DeploymentManager()
        self.ingress_manager = IngressManager()
        self.service = ServiceManager()
        self.config = {
            'name': 'test-deployment',
            'namespace': 'platform-enablement',
            'replicas': 2,
            'version': 'v0.1.6',
            'container': 'ikerry/metrics-node',
            'container_port': 8080,
            'dns_name': 'nodet.svc.platform.myobdev.com'
        }

    def test_get_simple_app(self):
        self.deployment.apply_namespaced_deployment(self.config)
        self.ingress.apply_namespaced_ingress(self.config)
        self.service.apply_namesapced_service(self.config)

    def tearDown(self):
        self.deployment.delete_namespaced_deployment(self.config)
        self.deployment.delete_namespaced_ingress(self.config)
        self.service.delete_namespaced_service(self.config)

        # Delete tls secret
        self.secret.delete_namespaced_secret({
            name: '{0}-tls'.format(self.config['name']),
            namespace: self.config['namespace']
        })

if __name__ == '__main__':
    unittest.main()


# - Verify simple app
#   - deploy 1 simple app
#   - test endpoints work with TLS
#   - Then
#       - teardown apps
