from unittest import TestCase
from python_nmcli_wrapper import NMCLI, NMCLI_EXIT_STATUS

class NmcliTests(TestCase):

    def test_00_constructor_0(self):
        nm = NMCLI()
        self.assertEqual(nm.path, '/usr/bin/nmcli')

    def test_00_constructor_1(self):
        nm = NMCLI(text=True)
        self.assertEqual(nm.text, True)

    def test_00_constructor_2(self):
        _env = {'LANG':'C'}
        nm = NMCLI(env=_env)
        self.assertEqual(nm.env, _env)

    def test_01_instance_raise_exception_0(self):
        with self.assertRaises(NameError):
            nm = NMCLI(path='/usr/local/not_nmcli')

    def test_01_instance_raise_exception_1(self):
        with self.assertRaises(TypeError):
            nm = NMCLI(text="Not boolean")

    def test_02_instance_raise_exception_2(self):
        with self.assertRaises(TypeError):
            nm = NMCLI(env="Not a dictionary")

    def test_02_show_version_0(self):
        nm = NMCLI()
        rc, stdout, stderr = nm.show_version()
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.split()[0], b'nmcli')

    def test_02_show_version_1(self):
        nm = NMCLI(text=True)
        rc, stdout, stderr = nm.show_version()
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.split()[0], 'nmcli')

    def test_02_show_version_2(self):
        nm = NMCLI(env={'LANG':'C'})
        rc, stdout, stderr = nm.show_version()
        self.assertEqual(rc, 0)
        self.assertEqual(stdout.split()[0:3], [b'nmcli', b'tool,', b'version'])

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

    def test_05_show_device_0(self):
        nm = NMCLI()
        _, dev, _ = nm.list_devices()
        d = dev[0].decode('utf8')

        rc, stdout, stderr = nm.show('device', d, field='all')
        self.assertEqual(rc, 0)
        self.assertEqual(type(stdout), dict)
        self.assertEqual(stdout[b'GENERAL.DEVICE'].decode('utf8'), d)

    def test_05_show_device_1(self):
        nm = NMCLI()
        _, dev, _ = nm.list_devices()
        d = dev[0].decode('utf8')

        rc, stdout, stderr = nm.show('device', d, field=('GENERAL.DEVICE', 'GENERAL.TYPE'))
        self.assertEqual(rc, 0)
        self.assertEqual(type(stdout), dict)
        self.assertEqual(stdout[b'GENERAL.DEVICE'].decode('utf8'), d)

    def test_06_show_connection_0(self):
        nm = NMCLI()
        _, con, _ = nm.list_connections()
        c = con[0].decode('utf8')

        rc, stdout, stderr = nm.show('connection', c, field='all')
        self.assertEqual(rc, 0)
        self.assertEqual(type(stdout), dict)
        self.assertEqual(stdout[b'connection.id'].decode('utf8'), c)

    def test_06_show_connection_1(self):
        nm = NMCLI()
        _, con, _ = nm.list_connections()
        c = con[0].decode('utf8')

        rc, stdout, stderr = nm.show('connection', c, field=['connection.id', 'connection.type'])
        self.assertEqual(rc, 0)
        self.assertEqual(type(stdout), dict)
        self.assertEqual(stdout[b'connection.id'].decode('utf8'), c)

    def test_07_add_connection_1(self):
        nm = NMCLI()
        ifname = 'dummy0'
        con_name = 'dummy-dummy0'
        ip_address = '192.0.2.1/24'
        dns_server = '1.1.1.1'

        rc, _, _ = nm.add_connection(
            'dummy',
            properties={
                'ifname':ifname, 'con-name':con_name,
                'ipv4.method':'manual', 'ipv4.addresses':ip_address,
                'ipv4.dns':dns_server,
            }
        )
        self.assertEqual(rc, 0)
        _, stdout, _ = nm.show('connection', con_name,
            field=','.join([
                'connection.interface-name',
                'connection.id',
                'ipv4.method',
                'ipv4.addresses'
            ])
        )
        self.assertEqual(stdout,
            {
                b'connection.interface-name':ifname.encode('utf8'),
                b'connection.id':con_name.encode('utf8'),
                b'ipv4.method':b'manual',
                b'ipv4.addresses':ip_address.encode('utf8')
            }
        )

    def test_08_modify_connection_1(self):
        nm = NMCLI()
        ipaddresses = ['198.51.100.1/24', '203.0.113.1/24']
        dnsservers = ['8.8.8.8', '8.8.4.4']

        rc, _, _ = nm.modify('connection', 'dummy-dummy0', {'+ipv4.addresses':ipaddresses, '+ipv4.dns':dnsservers})
        self.assertEqual(rc, 0)
        rc, stdout, stderr = nm.show('connection', 'dummy-dummy0', field='ipv4.addresses')
        self.assertEqual(stdout, {b'ipv4.addresses': b'192.0.2.1/24, 198.51.100.1/24, 203.0.113.1/24'})
        rc, stdout, stderr = nm.show('connection', 'dummy-dummy0', field='ipv4.dns')
        self.assertEqual(stdout, {b'ipv4.dns': b'1.1.1.1,8.8.8.8,8.8.4.4'})

    def test_08_modify_connection_2(self):
        nm = NMCLI()
        dns_server = ""

        rc, _, _ = nm.modify('connection', 'dummy-dummy0', {'ipv4.dns':dns_server})
        self.assertEqual(rc, 0)
        rc, stdout, stderr = nm.show('connection', 'dummy-dummy0', field='ipv4.dns')
        self.assertEqual(stdout, {b'ipv4.dns': b''})

    def test_09_up_connection(self):
        nm = NMCLI()

        _, before, _ = nm.show('device', 'dummy0', field='IP4.ADDRESS')
        rc, _, _ = nm.up_connection('dummy-dummy0')
        self.assertEqual(rc, 0)
        _, after, _ = nm.show('device', 'dummy0', field='IP4.ADDRESS')
        self.assertEqual(before[b'IP4.ADDRESS[1]'], after[b'IP4.ADDRESS[1]'])
        self.assertEqual(after[b'IP4.ADDRESS[2]'], b'198.51.100.1/24')
        self.assertEqual(after[b'IP4.ADDRESS[3]'], b'203.0.113.1/24')

    def test_10_delete_connection(self):
        nm = NMCLI()

        rc, _, _ = nm.delete_connection('dummy-dummy0')
        self.assertEqual(rc, 0)
        _, stdout, _ = nm.list_connections()
        self.assertNotIn(b'dummy-dummy0', stdout)

    def test_11_delete_device(self):
        nm = NMCLI()

        _, stdout, _ = nm.list_devices()
        if b'dummy0' in stdout:
            rc, _, _ = nm.delete_device('dummy0')
            self.assertEqual(rc, 0)

        self.assertNotIn(b'dummy0', stdout)

if __name__ == '__main__':
    main()
