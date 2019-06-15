import unittest
from kube.pod import PodManager

class TestPodsManager(unittest.TestCase):

    def setUp(self):
        self.pod_manager = PodManager()
        self.namespace = 'kube-system'

    def test_kube_system_pods_healthy(self):
        kube_system_pods = self.pod_manager.list_namespaced_pods(self.namespace)
        results = ['Running', 'Succeeded']
        for pod in kube_system_pods:
            statusResult = pod.status.phase in results
            if statusResult is False:
                print(pod.status)
            self.assertTrue(statusResult)

if __name__ == '__main__':
    unittest.main()
