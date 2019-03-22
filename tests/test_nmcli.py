from unittest import TestCase
from python_nmcli_wrapper import NMCLI, NMCLI_EXIT_STATUS

class NmcliTests(TestCase):

    def test_create_instance(self):
        nm = NMCLI()
        self.assertEqual(nm.path, '/usr/bin/nmcli')

    def test_instance_raise_exception(self):
        with self.assertRaises(NameError):
            nm = NMCLI(path='/usr/local/not_nmcli')

    def test_show_version(self):
        nm = NMCLI()
        rc, stdout, stderr = nm.show_version()
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.split()[0], 'nmcli')

if __name__ == '__main__':
    main()
