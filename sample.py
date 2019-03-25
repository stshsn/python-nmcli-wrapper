from python_nmcli_wrapper import NMCLI, NMCLI_EXIT_STATUS

nm = NMCLI()
returncode, stdout, stderr = nm.show_version()
print(stdout)

returncode, stdout, stderr = nm.list_devices()
print(stdout)

returncode, stdout, stderr = nm.list_connections()
print(stdout)

returncode, stdout, stderr = nm.show('device', 'ens33', field='common')
print(NMCLI_EXIT_STATUS(returncode), stdout, stderr.decode('utf8'))

returncode, stdout, stderr = nm.show('connection', 'ens33', field='connection.id,connection.type')
print(NMCLI_EXIT_STATUS(returncode), stdout, stderr.decode('utf8'))

returncode, stdout, stderr = nm.modify('device', 'ens38', properties={'ipv4.method':'auto', '-ipv4.addresses':'192.168.17.22', '-ipv4.dns':'8.8.8.8'})
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

returncode, stdout, stderr = nm.modify('connection', 'wired1', properties={'ipv4.method':'auto', '+ipv4.dns':('8.8.8.8', '8.8.4.4', '1.1.1.1')})
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

returncode, stdout, stderr = nm.add_connection('bridge', properties={'ifname':'br0', 'con-name':'bridge-br0', 'ipv4.method':'manual', 'ipv4.addresses':'172.18.0.1/16', 'bridge.stp':'no'})
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

returncode, stdout, stderr = nm.delete_connection('bridge-br0')
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

returncode, stdout, stderr = nm.clone_connection('wired1', 'new-connection')
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))
returncode, stdout, stderr = nm.delete_connection('new-connection')

returncode, stdout, stderr = nm.reload_connection()
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

returncode, stdout, stderr = nm.load_connection('./ifcfg-default')
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

if __name__ == '__main__':
    print("end of script.")

