import unittest
import os
from kube.resources.daemonset import DaemonsetManager

must_have = [
    {
        'cluster': 'europa-stg',
        'namespace': 'kube-system',
        'pods': [
            'cadvisor',
            'canal',
            'cloudsmith-login',
            'kiam-agent',
            'kiam-server',
            'kube-logging',
            'kube-proxy',
            'node-problem-detector',
            'prometheus-node-exporter'
        ]
    },
    {
        'cluster': 'dev-green',
        'namespace': 'kube-system',
        'pods': [
            'cadvisor',
            'canal',
            'cloudsmith-login',
            'kiam-agent',
            'kiam-server',
            'kube-logging',
            'kube-proxy',
            'node-problem-detector',
            'prometheus-node-exporter'
        ]
    }
]

class TestDaemonsetsManager(unittest.TestCase):

    def setUp(self):
        self.daemonset_manager = DaemonsetManager()
        self.cluster = os.getenv('cluster', 'europa-stg')

    def test_kube_system_daemonsets(self):
        for item in must_have:
            if item['cluster'] == self.cluster:
                daemonsets = self.daemonset_manager.list(item['namespace'])
                for pod in item['pods']:
                    print(f'daemonsets -> {self.cluster} {item["namespace"]}: {pod}')
                    self.assertIn(pod, daemonsets)

if __name__ == '__main__':
    unittest.main()
