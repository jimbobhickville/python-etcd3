"""
test_etcd3
----------------------------------

Tests for `etcd3` module.
"""

import json
import os
import subprocess

import pytest
from hypothesis import given
from hypothesis.strategies import characters
from hypothesis.strategies import text

import etcd3


os.environ['ETCDCTL_API'] = '3'


def etcdctl(*args):
    args = ['etcdctl', '-w', 'json'] + list(args)
    output = subprocess.check_output(args)
    return json.loads(output.decode('utf-8'))


class TestEtcd3(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_client_stub(self):
        etcd = etcd3.client()
        assert etcd is not None

    def test_get_unknown_key(self):
        etcd = etcd3.client()
        with pytest.raises(etcd3.exceptions.KeyNotFoundError):
            etcd.get('probably-invalid-key')

    @given(characters(blacklist_categories=['Cs', 'Cc']))
    def test_get_key(self, string):
        etcdctl('put', '/doot/a_key', string)
        etcd = etcd3.client()
        returned = etcd.get('/doot/a_key')
        assert returned == string.encode('utf-8')

    def test_put_key(self):
        etcd = etcd3.client()
        etcd.put('/doot/put_1', 'this is a doot')

    @classmethod
    def teardown_class(cls):
        etcdctl('del', '--prefix', '/doot')
