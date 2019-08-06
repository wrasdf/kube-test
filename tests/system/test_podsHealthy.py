import unittest
import os
from kube.utils.pod import PodManager

must_checks = [
    {
        'cluster': 'dev-green',
        'namespaces': [
            'kube-system',
            'kube-monitor'
        ]
    },
    {
        'cluster': 'europa-stg',
        'namespaces': [
            'kube-system',
            'kube-monitor'
        ]
    }
]

class TestPodsManager(unittest.TestCase):

    def setUp(self):
        self.pod_manager = PodManager()
        self.cluster = os.getenv('cluster', 'europa-stg')

    def test_kube_system_pods_healthy(self):
        for item in must_checks:
            if item['cluster'] == self.cluster:
                for ns in item['namespaces']:
                    system_pods = self.pod_manager.list(ns)
                    results = ['Running', 'Succeeded']
                    for pod in system_pods:
                        print(f'pod -> {self.cluster} {ns}: {pod.metadata.name}')
                        statusResult = pod.status.phase in results
                        if statusResult is False:
                            print(pod.status)
                        self.assertTrue(statusResult)

if __name__ == '__main__':
    unittest.main()
