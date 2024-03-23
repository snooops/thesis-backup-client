import pytest
from flask import g, session
import json
from jsonschema import validate


def test_generate_file_list(client, generate_backup_data):
    """Parameters client and generate_backup_data are pytest fixtures defined in conftest.py"""
    # getting the directory used for testing
    backup_dir = generate_backup_data
    
    # preparing json to sent
    data = {"path": backup_dir}
    
    # fire the request and save the response
    response =  client.post('/file/generate_file_list', json=data)

    # validate the http response code is 200
    assert response.status_code == 200

    # validate the json response
    with open('tests/testdata/file_list.json') as user_file:
        json_schema = json.load(user_file)
    validate(instance=response.json, schema=json_schema)

    