from python_nmcli_wrapper import NMCLI, NMCLI_EXIT_STATUS

"""
Create instance.

This module wrap 'nmcli' command that is expected in the path below.
    /usr/bin/nmcli
If your nmcli is in different path, you can specify the path using
'path' argument.
    nm = NMCLI(path='path/to/nmcli')

Throw NameError exception if path ending without 'nmcli'.
Throw FileNotFoundError if the file specified is not executable.


The return values except returncode described below are type of bytes.
If you want return values in type of str, you may specify 'text'
argument.
    nm = NMCLI(text=True)

Throw TypeError exception if you specify other than 'None', 'True' or
'False' for text argument.


If you want to pass environment variables when executing nmcli,
you can specify 'env' argument.
    nm = NMCLI(env={'LANG': 'C'})

Throw TypeError exception if you specify other than 'None' or
a dictionary.
"""
nm = NMCLI(text=True, env={'LANG':'C'})

"""
All methods return a tuple containing returncode, stdout and stderr.

returncode : exit status code from 'nmcli' command
stdout     : standard outout from 'nmcli' command
             some methods return a dict or list
stderr     : standard error output from 'nmcli'
             empty str is returned when 'nmcli' finished successfully
"""

# show version of 'nmcli'
returncode, stdout, stderr = nm.show_version()
print(stdout)


nm = NMCLI() # return values will be in type of bytes and default LOCALE
# show version of 'nmcli'
returncode, stdout, stderr = nm.show_version()
print(stdout)

# list devices recognised by NetworkManager
returncode, stdout, stderr = nm.list_devices()
print(stdout)

# list connections
returncode, stdout, stderr = nm.list_connections()
print(stdout)

# show device specified by name(i.e. ens33)
# Argument for 'field=' is used to specify what fields should be returned.
# Comma separated str(should be no white space), list or tuple is accepted.
returncode, stdout, stderr = nm.show('device', 'ens33', field='common')
print(NMCLI_EXIT_STATUS(returncode), stdout, stderr.decode('utf8'))

# show connection specified by name(i.e. ens33)
# Argument for 'field' is same explained above.
returncode, stdout, stderr = nm.show('connection', 'ens33', field='connection.id,connection.type')
print(NMCLI_EXIT_STATUS(returncode), stdout, stderr.decode('utf8'))

# modify device settings
# Target device is specified by name(i.e. ens38)
# Setting properties are specified by dict. The key is property name,
# the value is its value.
# Some properties are able to have multiple values. In this situation
# the values should be specified by list or tuple.
returncode, stdout, stderr = nm.modify('device', 'ens38', properties={'ipv4.method':'auto', '-ipv4.addresses':'192.168.17.22', '-ipv4.dns':'8.8.8.8'})
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

# modify connection settings
# Target connection is specified by name(i.e. wired1)
# Argument for properties is same explained above.
returncode, stdout, stderr = nm.modify('connection', 'wired1', properties={'ipv4.method':'auto', '+ipv4.dns':('8.8.8.8', '8.8.4.4', '1.1.1.1')})
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

# add a connection
# First argument is for connection name. It is must be specified.
# Argument for properties is same explainded above.
returncode, stdout, stderr = nm.add_connection('bridge', properties={'ifname':'br0', 'con-name':'bridge-br0', 'ipv4.method':'manual', 'ipv4.addresses':'172.18.0.1/16', 'bridge.stp':'no'})
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

# delete connection
# Specify the name of connection to delete.
returncode, stdout, stderr = nm.delete_connection('bridge-br0')
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

# clone connection
# First argument is name of connection to be cloned.
# Second argument is name of new cloned connection.
returncode, stdout, stderr = nm.clone_connection('wired1', 'new-connection')
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))
returncode, stdout, stderr = nm.delete_connection('new-connection')

# reload connection
# Reload all connection from disk.
returncode, stdout, stderr = nm.reload_connection()
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

# load connection
# Load/reload conenction files from disk.
# Path to configuration file is must be specified.
returncode, stdout, stderr = nm.load_connection('./ifcfg-default')
print(NMCLI_EXIT_STATUS(returncode), stdout.decode('utf8'), stderr.decode('utf8'))

if __name__ == '__main__':
    print("end of script.")

