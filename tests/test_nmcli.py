from unittest import TestCase
from python_nmcli_wrapper import NMCLI, NMCLI_EXIT_STATUS

class NmcliTests(TestCase):

    def test_00_constructor(self):
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

    def test_07_add_connection(self):
        nm = NMCLI()
        ifname = 'br0'
        con_name = 'bridge-br0'
        ip_address = '10.0.0.1/24'

        rc, _, _ = nm.add_connection(
            'bridge',
            properties={
                'ifname':ifname, 'con-name':con_name,
                'bridge.stp':'no',
                'ipv4.method':'manual', 'ipv4.addresses':ip_address,
            }
        )
        self.assertEqual(rc, 0)
        _, stdout, _ = nm.show('connection', con_name,
            field=','.join([
                'connection.interface-name',
                'connection.id',
                'bridge.stp',
                'ipv4.method',
                'ipv4.addresses'
        ]))
        self.assertEqual(stdout, {b'connection.interface-name':ifname.encode('utf8'), b'connection.id':con_name.encode('utf8'), b'bridge.stp':b'no', b'ipv4.method':b'manual', b'ipv4.addresses':ip_address.encode('utf8')})

    def test_08_modify_connection(self):
        nm = NMCLI()
        ipaddresses = ['10.0.0.2/24', '10.0.0.3/24']

        rc, _, _ = nm.modify('connection', 'bridge-br0', {'+ipv4.addresses':ipaddresses})
        self.assertEqual(rc, 0)
        rc, stdout, stderr = nm.show('connection', 'bridge-br0', field='ipv4.addresses')
        self.assertEqual(stdout, {b'ipv4.addresses': b'10.0.0.1/24, 10.0.0.2/24, 10.0.0.3/24'})

    def test_09_up_connection(self):
        nm = NMCLI()

        _, before, _ = nm.show('device', 'br0', field='IP4.ADDRESS')
        rc, _, _ = nm.up_connection('bridge-br0')
        self.assertEqual(rc, 0)
        _, after, _ = nm.show('device', 'br0', field='IP4.ADDRESS')
        self.assertEqual(before[b'IP4.ADDRESS[1]'], after[b'IP4.ADDRESS[1]'])
        self.assertEqual(after[b'IP4.ADDRESS[2]'], b'10.0.0.2/24')
        self.assertEqual(after[b'IP4.ADDRESS[3]'], b'10.0.0.3/24')

    def test_10_delete_connection(self):
        nm = NMCLI()

        rc, _, _ = nm.delete_connection('bridge-br0')
        self.assertEqual(rc, 0)
        _, stdout, _ = nm.list_connections()
        self.assertNotIn(b'bridge-br0', stdout)
        _, stdout, _ = nm.list_devices()
        self.assertNotIn(b'br0', stdout)

if __name__ == '__main__':
    main()
