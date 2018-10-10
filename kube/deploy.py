from kubernetes import client, config
from .config_manager import ConfigManager

class DeployManager:

    def __init__(self):
        ConfigManager()
        self.api = client.CoreV1Api()


# TODO:
# - Common scenario test
#   - deploy kube-demo into current cluster
#   - test ingress works
#   - delete the app
# - Kube2iam scenario test
#   - deploy kube2iam into current cluster
#   - test permission with s3 works
#   - delete the app
