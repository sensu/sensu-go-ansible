import errno
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import tempfile
import time

import pytest


def pytest_collect_file(parent, path):
    if path.basename.startswith('test_') and path.basename.endswith('.yml'):
        return PlaybookFile(path, parent)


class PlaybookFile(pytest.File):
    def collect(self):
        tmpdir = tempfile.mkdtemp(prefix='sensu-backend', dir='/var/tmp')

        # This is an irritating number of ports, which highlights the racy
        # nature of this approach.
        sensu_kwargs = {
            'port': openport(14567),
            'dashboard_port': openport(3000),
            'etcd_client_port': openport(2379),
            'etcd_peer_port': openport(12379),
            'datadir': os.path.join(tmpdir, 'sensu-backend'),
        }

        conf = '''log-level: debug
state-dir: {datadir}
cache-dir: {datadir}
api-listen-address: "[::]:{port}"
api-url: http://localhost:{port}
dashboard-port: {dashboard_port}
etcd-listen-client-urls: ["http://127.0.0.1:{etcd_client_port}"]
etcd-client-peer-urls: ["http://127.0.0.1:{etcd_peer_port}"]
'''.format(**sensu_kwargs)

        conf_file = os.path.join(tmpdir, 'backend.yml')
        with open(conf_file, 'w') as f:
            f.write(conf)

        devnull = open(os.devnull, 'w')
        sensu_proc = subprocess.Popen(['sensu-backend', 'start', '-c', conf_file], stdout=devnull, stderr=devnull)

        try:
            out = subprocess.check_output([
                'ansible-playbook', '-v',
                '-i', '/dev/null',
                '-e', 'sensu_port={}'.format(sensu_kwargs['port']),
                str(self.fspath),
            ])
        except subprocess.CalledProcessError as e:
            out = e.output

        sensu_proc.terminate()
        shutil.rmtree(tmpdir)
        time.sleep(1)

        started = False
        for line in out.split('\n'):
            if line.startswith('TASK'):
                new_name = re.match('TASK \[(.+)\] ', line).group(1)
                if new_name != 'assert':
                    name = new_name
            elif started:
                lines += line
                if line == '}':
                    yield PlaybookItem(self, name, state, lines)
                    started = False
            else:
                matches = re.match('([a-z]+): \[localhost\][^=>]+=> (.+)', line)
                if matches:
                    if matches.group(2) == '{':
                        started = True
                        state = matches.group(1)
                        lines = '{'
                    else:
                        yield PlaybookItem(self, name, matches.group(1), matches.group(2))


class PlaybookItem(pytest.Item):
    def __init__(self, parent, name, state, obj):
        super(PlaybookItem, self).__init__(name, parent)
        self.state = state
        self.obj = obj

    def runtest(self):
        self.json = json.loads(self.obj)
        if self.state not in ('ok', 'changed'):
            raise PlaybookError()

    def repr_failure(self, excinfo):
        if isinstance(excinfo.value, PlaybookError):
            return self.json
        return self._repr_failure_py(excinfo)


class PlaybookError(Exception):
    """ custom exception """


def openport(port):
    # Find a usable port by iterating until there's an unconnectable port
    while True:
        try:
            conn = socket.create_connection(('localhost', port), 0.1)
            port += 1
            if port > 65535:
                raise ValueError("exhausted TCP port range without finding a free one")
        except socket.error:
            return( port )
