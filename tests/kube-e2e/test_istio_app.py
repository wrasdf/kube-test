import unittest
import time
import requests
from kube.ingress import IngressManager
from kube.deployment import DeploymentManager
from kube.service import ServiceManager
from kube.secret import SecretManager
from kube.exec import EXEC

class TestNamespaceManager(unittest.TestCase):

    def setUp(self):
        self.exec = EXEC()
        self.deployment = DeploymentManager()
        self.ingress = IngressManager()
        self.service = ServiceManager()
        self.secret = SecretManager()
        self.config = {
            'name': 'node1-deployment',
            'namespace': 'platform-enablement',
            'replicas': 1,
            'version': 'v0.1.6',
            'container': 'ikerry/metrics-node',
            'container_port': 8080,
            'dns_name': 'node1.svc.platform.myobdev.com'
        }

    def test_istio_app(self):

        # Deploy node1
        self.deployment.apply_namespaced_deployment(self.config)
        self.ingress.apply_namespaced_ingress(self.config)
        self.service.apply_namesapced_service(self.config)

        # # Deploy node2
        node2Config = dict(self.config, **{
            'name': 'node2-deployment',
            'dns_name': 'node2.svc.platform.myobdev.com'
        })
        self.deployment.apply_namespaced_deployment(node2Config)
        self.ingress.apply_namespaced_ingress(node2Config)
        self.service.apply_namesapced_service(node2Config)

        # Deploy node3
        node3Config = dict(self.config, **{
            'name': 'node3-deployment',
            'dns_name': 'node3.svc.platform.myobdev.com',
            'sidecarEnable': 'true'
        })
        self.deployment.apply_namespaced_deployment(node3Config)
        self.ingress.apply_namespaced_ingress(node3Config)
        self.service.apply_namesapced_service(node3Config)

        # Deploy node4
        node4Config = dict(self.config, **{
            'name': 'node4-deployment',
            'dns_name': 'node4.svc.platform.myobdev.com',
            'sidecarEnable': 'true'
        })
        self.deployment.apply_namespaced_deployment(node4Config)
        self.ingress.apply_namespaced_ingress(node4Config)
        self.service.apply_namesapced_service(node4Config)

        # Todo install destination rules for node3 & node4


        # wait for 60 seconds cert-manager to generate tls certs
        time.sleep(60)

        # response = requests.get("https://{0}/api/v1/health".format(self.config['dns_name']))
        # self.assertEqual(200, response.status_code)
        # self.assertEqual('OK!', response.text)

    def tearDown(self):
        self.deployment.delete_namespaced_deployment(self.config)
        self.ingress.delete_namespaced_ingress(self.config)
        self.service.delete_namespaced_service(self.config)

        # Delete tls secret
        self.secret.delete_namespaced_secret({
            'name': '{0}-tls'.format(self.config['name']),
            'namespace': self.config['namespace']
        })

if __name__ == '__main__':
    unittest.main()


# - Verify Istio app
#   - deploy 2 simple app without sidecar
#   - deploy 2 simple app with sidecar
#   - test endpoints work with TLS
#   - test services level communication works
#     - with sidecar could talk to with sidecar
#     - with sidecar could talk to without sidecar
#     - without sidecar could talk to with sidecar
#     - without sidecar could talk to without sidecar
#   - Then
#       - teardown apps
