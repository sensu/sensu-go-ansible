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
        port = openport(14567)

        tmpdir = tempfile.mkdtemp(prefix='sensu-backend', dir='/var/tmp')

        conf = os.path.join(tmpdir, 'backend.yml')
        datadir = os.path.join(tmpdir, 'sensu-backend')

        with open(conf, 'w') as f:
            f.write('log-level: debug\n')
            f.write('state-dir: {}\n'.format(datadir))
            f.write('cache-dir: {}\n'.format(datadir))
            f.write('api-listen-address: "[::]:{}"\n'.format(port))
            f.write('api-url: http://localhost:{}\n'.format(port))

        devnull = open(os.devnull, 'w')
        sensu_proc = subprocess.Popen(['sensu-backend', 'start', '-c', conf], stdout=devnull, stderr=devnull)

        try:
            out = subprocess.check_output([
                'ansible-playbook', '-v',
                '-i', '/dev/null',
                '-e', 'sensu_port={}'.format(port),
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
