import pytest
from flask import g, session


@pytest.mark.parametrize(('path'), (
    ("/home/snooops/thesis-backup-test-dir", b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_generate_file_list(client, path):
    data = {"path": "/home/snooops/thesis-backup-test-dir"}
    assert client.post('/file/generate_file_list', json=data)