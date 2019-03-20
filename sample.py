from nmcli import NMCLI, NMCLI_EXIT_STATUS

nm = NMCLI()
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

if __name__ == '__main__':
    print("end of script.")

