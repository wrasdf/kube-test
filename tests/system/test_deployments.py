import unittest
import os
from kube.resources.deployment import DeploymentManager


must_have = [
    {
        'cluster': 'europa-stg',
        'namespace': 'kube-system',
        'deploys': [
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
            'metrics-server',
            'kube-state-metrics',
            'cloudwatch-exporter',
            'aws-limits-exporter',
            'prometheus-alert-pipeline-monitor',

            #logs
            'kube-logging-events'
        ]
    },
    {
        'cluster': 'europa-stg',
        'namespace': 'kube-monitor',
        'deploys': [
            'external-metrics-apiserver',
            'grafana'
        ]
    },
    {
        'cluster': 'dev-green',
        'namespace': 'kube-system',
        'deploys': [
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
            'metrics-server',
            'kube-state-metrics',
            'cloudwatch-exporter',
            'aws-limits-exporter',
            'prometheus-alert-pipeline-monitor',

            #logs
            'kube-logging-events'
        ]
    },
    {
        'cluster': 'dev-green',
        'namespace': 'kube-monitor',
        'deploys': [
            'external-metrics-apiserver',
            'grafana'
        ]
    }
]

class TestDeploymentsManager(unittest.TestCase):
    def setUp(self):
        self.deploy_manager = DeploymentManager()
        self.cluster = os.getenv('cluster', 'europa-stg')

    def test_kube_system_deployment(self):
        for item in must_have:
            if item['cluster'] == self.cluster:
                deploys = self.deploy_manager.list(item['namespace'])
                for deploy in item['deploys']:
                    print(f'deploy -> {self.cluster} {item["namespace"]} {deploy} ')
                    self.assertIn(deploy, deploys)

if __name__ == '__main__':
    unittest.main()
