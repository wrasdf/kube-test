import unittest
from kube.pod import PodManager

class TestPodsManager(unittest.TestCase):

    def setUp(self):
        self.pod_manager = PodManager()
        self.namespace = 'kube-system'

    def test_kube_system_pods_healthy(self):
        kube_system_pods = self.pod_manager.list_namespaced_pods(self.namespace)
        for pod in kube_system_pods:
            self.assertEqual(pod.status.phase, 'Running')

if __name__ == '__main__':
    unittest.main()
