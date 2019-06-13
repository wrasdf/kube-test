import unittest
from kube.daemonset import DaemonsetManager

must_have_daemonsets = [
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

class TestDaemonsetsManager(unittest.TestCase):

    def setUp(self):
        self.daemonset_manager = DaemonsetManager()
        self.namespace = 'kube-system'

    def test_kube_system_daemonsets(self):
        self.kube_system_daemonsets = self.daemonset_manager.list_namespaced_daemonsets(self.namespace)
        for daemonsets in must_have_daemonsets:
            self.assertIn(daemonsets, self.kube_system_daemonsets)

if __name__ == '__main__':
    unittest.main()
