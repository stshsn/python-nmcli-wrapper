import os, shlex, subprocess, re
from enum import Enum

def _run_nmcli(nmcli):
    cmd = ' '.join([nmcli.path, nmcli.args])
    args = shlex.split(cmd)

    process = subprocess.run(args, capture_output=True, text=nmcli.text, env=nmcli.env)

    returncode = process.returncode
    stdout = process.stdout
    stderr = process.stderr

    return returncode, stdout, stderr

def __multiple_values_to_list__(params, text):
    if type(params) is not dict:
        raise TypeError("Except 'dict' for argument 'params'.")

    key_name = b'(?P<key_name>.+)\[[0-9]+\]$'
    if text is True:
        key_name = key_name.decode('UTF-8')
    for k in list(params):
        match = re.search(key_name, k)
        if match:
            params.setdefault(match.group('key_name'), []).append(params[k])

    return params

class NMCLI(object):
    def __init__(self, *, path='/usr/bin/nmcli', text=None, env=None, sudo=False):
        if os.path.basename(path) != 'nmcli':
            raise NameError("'{path}' is not a path to nmcli.".format(path=path))
        if os.access(path, os.X_OK):
            self.path = path
            self.args = ''
        else:
            raise FileNotFoundError("'{path}' is not executable.".format(path=path))
        if text is None or type(text) is bool:
            self.text = text
        else:
            raise TypeError("Except 'None or bool' for argument 'text'.")
        if env is None:
            self.env = None
        elif type(env) is dict:
            self.env = env
        else:
            raise TypeError("Except 'dict' for argument 'env'.")
        if sudo is not False:
            if os.path.basename(sudo) != 'sudo':
                raise NameError("'{sudo}' is not a path to sudo.".format(sudo=sudo))
            if os.access(path, os.X_OK):
                self.sudo = sudo
            else:
                raise FileNotFoundError("'{sudo}' is not executable.".format(sudo=sudo))
            self.path = self.sudo + ' ' + self.path

    def show_version(self):
        self.args = '-v'
        rc, stdout, stderr = _run_nmcli(self)
        return rc, stdout, stderr

    def list_devices(self):
        self.args = '-g DEVICE device'
        rc, stdout, stderr = _run_nmcli(self)

        if rc == 0:
            devices = tuple(stdout.splitlines())
        else:
            devices = None
        
        return rc, devices, stderr

    def list_connections(self):
        self.args = '-g NAME connection'
        rc, stdout, stderr = _run_nmcli(self)

        if rc == 0:
            connections = tuple(stdout.splitlines())
        else:
            connections = None

        return rc, connections, stderr

    def show(self, target, id, field='common'):
        if type(field) is str:
            field = field.replace(" ", "")
        elif type(field) in (list, tuple):
            field = ','.join(field)
        else:
            raise TypeError("Expected 'list', 'tuple' or 'str' for argument 'field'.")

        self.args = '-t -f {field} {target} show {id}'.format(field=field, target=target, id=id)
        rc, stdout, stderr = _run_nmcli(self)

        if rc == 0:
            params = dict()
            delimiter = b':'
            if self.text is True:
                delimiter = delimiter.decode('UTF-8')
            for f in stdout.splitlines():
                key, value = f.split(delimiter, 1)
                params[key] = value
            if target == 'device':
                params = __multiple_values_to_list__(params, self.text)
        else:
            params = None

        return rc, params, stderr

    def modify(self, target, id, properties=None):
        self.args = '{target} modify {id}'.format(target=target, id=id)

        if type(properties) is not dict:
            raise TypeError("'properties' must be dictionary.")
        else:
            for p, v in properties.items():
                if type(v) in (list, tuple):
                    for ev in v:
                        self.args += ' {p} {ev}'.format(p=p, ev=ev)
                elif type(v) is str:
                    if len(v) == 0:
                        self.args += ' {p} ""'.format(p=p)
                    else:
                        self.args += ' {p} {v}'.format(p=p, v=v)
                else:
                    raise TypeError("Expected 'list', 'tuple' or 'str' for argument 'values'.")

        rc, stdout, stderr = _run_nmcli(self)

        return rc, stdout, stderr

    def add_connection(self, connection_type, properties=None):
        self.args = 'connection add type {type}'.format(type=connection_type)

        if type(properties) is not dict:
            raise TypeError("'properties' must be dictionary.")
        else:
            for p, v in properties.items():
                if type(v) in (list, tuple):
                    for ev in v:
                        self.args += ' {p} {ev}'.format(p=p, ev=ev)
                elif type(v) is str:
                    if len(v) == 0:
                        self.args += ' {p} ""'.format(p=p)
                    else:
                        self.args += ' {p} {v}'.format(p=p, v=v)
                else:
                    raise TypeError("Expected 'list', 'tuple' or 'str' for argument 'values'.")

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
