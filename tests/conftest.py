import pytest
from backupclient import create_app
import os
import subprocess
import shutil

@pytest.fixture
def app():
    # bootstrap the app
    app = create_app()
    yield app

@pytest.fixture
def generate_backup_data(backup_path):
    
    os.makedirs(backup_path)
    os.makedirs(f"{backup_path}/subdir")

    with open(f'{backup_path}/subdir/hello.md', 'w') as f:
        f.write('Hello World!')
    
    with open(f'{backup_path}/subdir/secondfile.md', 'w') as f:
        f.write('A second file')

    with open(f'{backup_path}/README.md', 'w') as f:
        f.write('This directory is used by the backup-client unittest, and can be deleted.')

    with open(f'{backup_path}/a-dummy.md', 'w') as f:
        f.write('Lorem Ipsum dolor sit amet.')

    # now create a binary file
    summary = subprocess.check_output(
        ['dd', 'if=/dev/zero', f'of={backup_path}/binary.img', 'bs=64k', 'count=128'], stderr=subprocess.STDOUT)

    yield backup_path

    shutil.rmtree(backup_path)
    
@pytest.fixture
def backup_path():
    # creating some dummy data
    home_dir = os.path.expanduser('~')
    t_b_c = f"{home_dir}/test_thesis-backup-client"
    return t_b_c

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()