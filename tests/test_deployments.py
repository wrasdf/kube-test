import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, '../kube'))

import unittest
from deployment import DeploymentManager

must_have_deploys = [
    # system
    'kube-dns',
    'kube-dns-autoscaler',
    'dns-controller',
    'cluster-autoscaler',
    'cert-manager',
    'kube-lego',
    'ingress-nodeport',
    'nodeport-default-backend',

    # operators
    'db-operator',
    'alerting-rules-operator',

    # monitoring
    'grafana',
    'heapster',
    'kube-state-metrics',
    'kubernetes-dashboard-adfs',
    'monitoring-influxdb',
    'prometheus-alert-pipeline-monitor',
    'prometheus-alertmanager',
    'prometheus-server',

    #logs
    'cloudwatch-exporter'
    ]

class TestDeploymentsManager(unittest.TestCase):

    def setUp(self):
        self.deploy_manager = DeploymentManager()

    def test_kube_system_deployment(self):
        self.kube_system_deploys = self.deploy_manager.list_namespaced_deployments('kube-system')
        for deploy in must_have_deploys:
            self.assertIn(deploy, self.kube_system_deploys)

if __name__ == '__main__':
    unittest.main()
