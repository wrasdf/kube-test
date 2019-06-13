import unittest
from kube.deployment import DeploymentManager

must_have_deploys = [
    # system
    'dex',
    'cert-manager',
    'coredns',
    'velero',
    'ingress-nodeport',
    'kubernetes-dashboard-adfs',
    'cluster-autoscaler',
    'cluster-overprovisioner',
    'smooth-updater',
    'node-drainer',

    # operators
    'db-operator',
    'sqs-operator',
    'alerting-rules-operator',

    # monitoring
    'grafana',
    'metrics-server',
    'kube-state-metrics',
    'cloudwatch-exporter',
    'aws-limits-exporter',
    'prometheus-alert-pipeline-monitor',

    #logs
    'kube-logging-events'
    ]

class TestDeploymentsManager(unittest.TestCase):

    def setUp(self):
        self.deploy_manager = DeploymentManager()
        self.namespace = 'kube-system'

    def test_kube_system_deployment(self):
        self.kube_system_deploys = self.deploy_manager.list_namespaced_deployments(self.namespace)
        for deploy in must_have_deploys:
            self.assertIn(deploy, self.kube_system_deploys)

if __name__ == '__main__':
    unittest.main()
