from flask import current_app
import requests

from .test_blockstackauth import TOKEN_1, TOKEN_2, TOKEN_3
import os

image1 = "4eb9a451-2be6-4f98-bb62-3d5673d0c120.png"
#image2 = "88c0bc0a-c673-4cdf-8216-cd4e2c916be2.png"


def test_file_get(client):
    res = client.get('/api/file/{}'.format(image1))

    image = open(os.path.join(current_app.config['UPLOAD_FOLDER'], image1), "rb")
    image_data = image.read()
    image.close()

    assert res.status_code == 200
    assert res.data == image_data


def test_file_get_invalid_file(client):
    res = client.get('/api/file/im_really_not_there_i_promise_2391094i12093.png')

    assert res.status_code == 404


def test_file_get_path_traversal(client):
    res=client.get('/api/file/../.gitignore')

    file = open(os.path.join(current_app.config['ROOT_DIR'], ".gitignore"), "rb")
    file_data = file.read()
    file.close()

    assert res.data != file_data
    assert res.status_code == 404


def test_file_post(client):
    res = client.get('/api/file/dummy')

    headers = {"authToken": TOKEN_1, "idInstitution": "1", "idProject": "1"}
    file = open(os.path.join(current_app.config['TEST_UPLOAD_FOLDER'], "cat.png"), "rb")
    data = {'file': file}

    res=client.post('/api/file', headers=headers, data=data)

    assert res.status_code == 201

    # Open file again because its getting closed
    file = open(os.path.join(current_app.config['TEST_UPLOAD_FOLDER'], "cat.png"), "rb")
    file_data = file.read()

    # Cleanup
    for r, d, f in os.walk(current_app.config['UPLOAD_FOLDER']):
        for item in f:
            currFile_path = os.path.join(r, item)
            currFile = open(currFile_path, "rb")
            currFile_data = currFile.read()

            # Search the testfile (by comparing data) and delete it
            if currFile_data == file_data:
                currFile.close()
                os.remove(currFile_path)
            else:
                currFile.close()

    file.close()


def test_file_post_wrong_user(client):
    res = client.get('/api/file/dummy')

    headers = {"authToken": TOKEN_2, "idInstitution": "1", "idProject": "1"}
    file = open(os.path.join(current_app.config['TEST_UPLOAD_FOLDER'], "cat.png"), "rb")
    data = {'file': file}

    res = client.post('/api/file', headers=headers, data=data)

    assert res.status_code == 404

    file.close()


def test_file_post_wout_auth(client):
    res = client.get('/api/file/dummy')

    headers = {"idInstitution": "1", "idProject": "1"}
    file = open(os.path.join(current_app.config['TEST_UPLOAD_FOLDER'], "cat.png"), "rb")
    data = {'file': file}

    res = client.post('/api/file', headers=headers, data=data)
    file.close()

    assert res.status_code == 401


def test_file_post_missing_params(client):
    res = client.get('/api/file/dummy')

    headers = {"authToken": TOKEN_1}
    file = open(os.path.join(current_app.config['TEST_UPLOAD_FOLDER'], "cat.png"), "rb")
    data = {'file': file}

    res = client.post('/api/file', headers=headers, data=data)
    file.close()

    assert res.status_code == 400


def test_file_post_wrong_extension(client):
    res = client.get('/api/file/dummy')

    headers = {"authToken": TOKEN_1, "idInstitution": "1", "idProject": "1"}
    file = open(os.path.join(current_app.config['TEST_UPLOAD_FOLDER'], "cat.asd"), "rb")
    data = {'file': file}

    res = client.post('/api/file', headers=headers, data=data)
    file.close()

    assert res.status_code == 403

