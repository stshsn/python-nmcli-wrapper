import os, shlex, subprocess
from enum import Enum

def _run_nmcli(nmcli):
    cmd = nmcli.path + ' ' + nmcli.args
    args = shlex.split(cmd)

    process = subprocess.run(args, capture_output=True)

    returncode = process.returncode
    stdout = process.stdout
    stderr = process.stderr

    return returncode, stdout, stderr

class NMCLI(object):
    def __init__(self, path='/usr/bin/nmcli'):
        if os.path.basename(path) != 'nmcli':
            raise NameError("'{path}' is not a path to nmcli.".format(path=path))
        if os.access(path, os.X_OK):
            self.path = path
            self.args = ''
        else:
            raise FileNotFoundError("'{path}' is not executable.".format(path=path))

    def show_version(self):
        self.args = '-v'
        rc, stdout, stderr = _run_nmcli(self)
        return rc, stdout.decode('utf8'), stderr.decode('utf8')

    def list_devices(self):
        self.args = '-g DEVICE device'
        rc, stdout, stderr = _run_nmcli(self)

        if rc == 0:
            devices = tuple(stdout.splitlines())
        else:
            devices = None
        
        return rc, devices, stderr.decode('utf8')

    def list_connections(self):
        self.args = '-g NAME connection'
        rc, stdout, stderr = _run_nmcli(self)

        if rc == 0:
            connections = tuple(stdout.splitlines())
        else:
            connections = None

        return rc, connections, stderr.decode('utf8')

    def show(self, target, id, field='common'):
        self.args = '-t -f {field} {target} show {id}'.format(field=field, target=target, id=id)
        rc, stdout, stderr = _run_nmcli(self)

        if rc == 0:
            params = dict()
            for f in stdout.splitlines():
                key, value = f.split(b':', 1)
                params[key] = value
        else:
            params = None

        return rc, params, stderr

    def modify(self, target, id, properties=None):
        self.args = '{target} modify {id}'.format(target=target, id=id)

        if type(properties) is not dict:
            raise TypeError("'properties' must be dictionary.")
        else:
            for p, v in properties.items():
                self.args += ' {p} {v}'.format(p=p, v=v)

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def add_connection(self, connection_type, properties=None):
        self.args = 'connection add type {type}'.format(type=connection_type)

        if type(properties) is not dict:
            raise TypeError("'properties' must be dictionary.")
        else:
            for p, v in properties.items():
                self.args += ' {p} {v}'.format(p=p, v=v)

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def delete_connection(self, id):
        self.args = 'connection delete {id}'.format(id=id)

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def clone_connection(self, id, new_name):
        self.args = 'connection clone {id} {new_name}'.format(id=id, new_name=new_name)

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def reload_connection(self):
        self.args = 'connection reload'

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def load_connection(self, filename):
        self.args = 'connection load {filename}'.format(filename=filename)

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def up_connection(self, id):
        self.args = 'connection up {id}'.format(id=id)

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def down_connection(self, id):
        self.args = 'connection down {id}'.format(id=id)

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def reapply_device(self, ifname):
        self.args = 'device reapply {ifname}'.format(ifname=ifname)

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def connect_device(self, ifname, wait=90):
        self.args = '--wait={wait} device connect {ifname}'.format(wait=wait, ifname=ifname)

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def disconnect_device(self, ifname, wait=10):
        self.args = '--wait={wait} device disconnect {ifname}'.format(wait=wait, ifname=ifname)

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def delete_device(self, ifname, wait=10):
        self.args = '--wait={wait} device delete {ifname}'.format(wait=wait, ifname=ifname)

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

class NMCLI_EXIT_STATUS(Enum):
    SUCCESS = 0
    UNKNOWN = 1
    INVALID_USER_INPUT = 2
    TIMEOUT_EXPIRED = 3
    CONNECTION_ACTIVATION_FAILED = 4
    CONNECTION_DEACTIVATION_FAILED = 5
    DISCONNECTING_DEVICE_FAILED = 6
    CONNECTION_DELETION_FAILED = 7
    NETWORKMANAGER_IS_NOT_RUNNING = 8
    DOES_NOT_EXIST = 10
    COMPLETE_ARGS = 65

if __name__ == '__main__':
    nmcli_instance = NMCLI()
    rc, stdout, stderr = nmcli_instance.show_version()

    if rc == 0:
        print(stdout, end="")
    else:
        print("return code[{rc}]: {stderr}".format(rc=rc, stderr=stderr), end="")
