import os
import importlib

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("deployment", os.path.join(
    current_dir, "deployment.py")).load_module()
importlib.machinery.SourceFileLoader("ingress", os.path.join(
    current_dir, "ingress.py")).load_module()

from ingress import IngressManager
from deployment import DeploymentManager

class DeployManager:

    def __init__(self):
        self.deployment = DeploymentManager()
        self.ingress = IngressManager()
        self.config = {
            'name': 'test-deployment',
            'namespace': 'platform-enablement',
            'replicas': 2,
            'version': 'v0.1.6',
            'container': 'ikerry/metrics-node',
            'container_port': 8080,
            'dns_name': 'nodet.svc.platform.myobdev.com'
        }
    def apply(self, params):
        self.deployment.apply_deployment(params)
        self.ingress.apply_ingress(params)



# de = DeployManager()
# de.apply(de.config)


# TODO:
# - Common scenario test
#   - deploy kube-demo into current cluster
#   - test ingress works
#   - delete the app
# - kiam scenario test
#   - deploy kiam into current cluster
#   - test permission with s3 works
#   - delete the app
