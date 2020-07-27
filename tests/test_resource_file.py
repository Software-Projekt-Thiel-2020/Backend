from flask import current_app

from .test_blockstackauth import TOKEN_1, TOKEN_2, TOKEN_3
import os

# 88c0bc0a-c673-4cdf-8216-cd4e2c916be2.png
image1 = "4eb9a451-2be6-4f98-bb62-3d5673d0c120.png"

def test_file_get(client):
    res = client.get('/api/file/{}'.format(image1))

    try:
        image = open(os.path.join(current_app.config['UPLOAD_FOLDER'], image1), "rb")
        image_data = image.read()
    except:
        print("exception in test_file_get (file operations)")
    finally:
        image.close()

    assert res.status_code == 200
    assert res.data == image_data


def test_file_get_invalid_file(client):
    res = client.get('/api/file/im_really_not_there_i_promise_2391094i12093.png')

    assert res.status_code == 404


def test_file_get_path_traversal(client):
    res=client.get('/api/file/../.gitignore')

    try:
        file = open(os.path.join(current_app.config['ROOT_DIR'], ".gitignore"), "rb")
        file_data = file.read()
    except:
        print("exception in test_file_get_path_traversal")
    finally:
        file.close()

    assert res.data != file_data
    assert res.status_code == 404

