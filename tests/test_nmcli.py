from unittest import TestCase
from python_nmcli_wrapper import NMCLI, NMCLI_EXIT_STATUS

class NmcliTests(TestCase):

    def test_00_create_instance(self):
        nm = NMCLI()
        self.assertEqual(nm.path, '/usr/bin/nmcli')

    def test_01_instance_raise_exception(self):
        with self.assertRaises(NameError):
            nm = NMCLI(path='/usr/local/not_nmcli')

    def test_02_show_version(self):
        nm = NMCLI()
        rc, stdout, stderr = nm.show_version()
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.split()[0], 'nmcli')

    def test_03_list_devices(self):
        nm = NMCLI()
        rc, stdout, stderr = nm.list_devices()
        self.assertEqual(rc, 0)
        self.assertEqual(type(stdout), tuple)

    def test_04_list_connections(self):
        nm = NMCLI()
        rc, stdout, stderr = nm.list_devices()
        self.assertEqual(rc, 0)
        self.assertEqual(type(stdout), tuple)

    def test_05_show_device(self):
        nm = NMCLI()
        _, dev, _ = nm.list_devices()
        d = dev[0].decode('utf8')

        rc, stdout, stderr = nm.show('device', d, field='all')
        self.assertEqual(rc, 0)
        self.assertEqual(type(stdout), dict)
        self.assertEqual(stdout[b'GENERAL.DEVICE'].decode('utf8'), d)

    def test_06_show_connection(self):
        nm = NMCLI()
        _, con, _ = nm.list_connections()
        c = con[0].decode('utf8')

        rc, stdout, stderr = nm.show('connection', c, field='all')
        self.assertEqual(rc, 0)
        self.assertEqual(type(stdout), dict)
        self.assertEqual(stdout[b'connection.id'].decode('utf8'), c)

if __name__ == '__main__':
    main()
