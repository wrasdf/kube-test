import os
import importlib

current_dir = os.path.dirname(__file__)
importlib.machinery.SourceFileLoader("deployment", os.path.join(current_dir, "deployment.py")).load_module()
importlib.machinery.SourceFileLoader("ingress", os.path.join(current_dir, "ingress.py")).load_module()
importlib.machinery.SourceFileLoader("service", os.path.join(current_dir, "service.py")).load_module()
from deployment import DeploymentManager
from ingress import IngressManager
from service import ServiceManager

class DeployManager:

    def __init__(self):
        self.deployment = DeploymentManager()
        self.ingress = IngressManager()
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

    def apply(self):
        self.deployment.apply_namespaced_deployment(self.config)
        self.ingress.apply_namespaced_ingress(self.config)
        self.service.apply_namesapced_service(self.config)

    def delete(self):
        self.deployment.delete_namespaced_deployment(self.config)
        self.deployment.delete_namespaced_ingress(self.config)
        self.service.delete_namespaced_service(self.config)


# de = DeployManager()
# de.apply()
# de.delete()
