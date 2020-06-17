"""Tests for resource institutions."""
from tests.test_blockstackauth import TOKEN_1, TOKEN_2, TOKEN_3


def test_institutions_get(client):
    res = client.get('/api/institutions')
    assert res._status_code == 200
    assert len(res.json) == 4

    assert res.json[0]["id"] == 1
    assert res.json[0]["name"] == "MSGraphic"
    assert res.json[0]["webpage"] == "www.msgraphic.com"
    assert res.json[0]["address"] == "Address1"

    assert res.json[1]["id"] == 2
    assert res.json[1]["name"] == "SWP"
    assert res.json[1]["webpage"] == "www.swp.com"
    assert res.json[1]["address"] == "Address2"

    assert res.json[2]["id"] == 3
    assert res.json[2]["name"] == "Asgard Inc."
    assert res.json[2]["webpage"] == "www.asgard.as"
    assert res.json[2]["address"] == "Address3"

    assert res.json[3]["id"] == 4
    assert res.json[3]["name"] == "Blackhole"
    assert res.json[3]["webpage"] == "127.0.0.1"
    assert res.json[3]["address"] == "Address4"


def test_institutions_get_id(client):
    res = client.get('/api/institutions?id=1')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["name"] == "MSGraphic"
    assert res.json[0]["webpage"] == "www.msgraphic.com"
    assert res.json[0]["address"] == "Address1"


def test_institutions_get_bad_id(client):
    res = client.get('/api/institutions?id=1337')
    assert res._status_code == 200
    assert len(res.json) == 0


def test_institutions_post(client):
    headers = {"authToken": TOKEN_1, "username": "sw2020testuser2.id.blockstack", "name": "ExampleInstitution",
               "address": "Address"}
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde erstellt"

    res = client.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["name"] == "ExampleInstitution"
    assert res.json[0]["webpage"] is None
    assert res.json[0]["address"] == "Address"


def test_institutions_post2(client):
    headers = {"authToken": TOKEN_1, "username": "sw2020testuser2.id.blockstack", "name": "ExampleInstitution",
               "address": "Address",
               "webpage": "https://www.example.com/"}
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde erstellt"

    res = client.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["name"] == "ExampleInstitution"
    assert res.json[0]["webpage"] == "https://www.example.com/"
    assert res.json[0]["address"] == "Address"


def test_institutions_post_bad_owner(client):
    headers = {"authToken": TOKEN_1, "username": "sw2020testuser1337.id.blockstack", "name": "ExampleInstitution",
               "address": "Address",
               "webpage": "https://www.example.com/"}
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "username not found"


def test_institutions_post_non_support_user(client):
    headers = {"authToken": TOKEN_2, "username": "sw2020testuser2.id.blockstack", "name": "ExampleInstitution",
               "address": "Address",
               "webpage": "https://www.example.com/"}
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 403
    assert len(res.json) == 1
    assert res.json["error"] == "Forbidden"


def test_institutions_post_no_auth(client):
    headers = {}
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 401


def test_institutions_post_no_params(client):
    headers = {"authToken": TOKEN_1, }
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "Missing parameter"


def test_institutions_post_bad_webpage(client):
    headers = {"authToken": TOKEN_1, "name": "ExampleInstitution", "address": "Address",
               "webpage": "NotAValidURL"}
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "webpage is not a valid url"


def test_institutions_post_existing_name(client):
    headers = {"authToken": TOKEN_1, "username": "sw2020testuser2.id.blockstack", "name": "MSGraphic",
               "address": "Address",
               "webpage": "https://www.example.com/"}
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "name already exists"


def test_institutions_patch(client):
    test_institutions_post2(client)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5, "name": "NewExampleInstitution", "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client.patch('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde bearbeitet"

    res = client.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["name"] == "NewExampleInstitution"
    assert res.json[0]["webpage"] == "https://www.new_example.com/"
    assert res.json[0]["address"] == "NewAddress"


def test_institutions_patch2(client):
    test_institutions_post2(client)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5, "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client.patch('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde bearbeitet"

    res = client.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["name"] == "ExampleInstitution"
    assert res.json[0]["webpage"] == "https://www.new_example.com/"
    assert res.json[0]["address"] == "NewAddress"


def test_institutions_patch3(client):
    test_institutions_post2(client)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5, "webpage": "https://www.new_example.com/"}
    res = client.patch('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde bearbeitet"

    res = client.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["name"] == "ExampleInstitution"
    assert res.json[0]["webpage"] == "https://www.new_example.com/"
    assert res.json[0]["address"] == "Address"


def test_institutions_patch_missing_id(client):
    test_institutions_post2(client)  # create institution

    headers = {"authToken": TOKEN_2, "name": "NewExampleInstitution", "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client.patch('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "Missing parameter"


def test_institutions_patch_name_exists(client):
    test_institutions_post2(client)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5, "name": "MSGraphic", "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client.patch('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "name already exists"


def test_institutions_patch_id_doesnt_exist(client):
    headers = {"authToken": TOKEN_2, "id": 5, "name": "NewExampleInstitution", "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client.patch('/api/institutions', headers=headers)
    assert res._status_code == 404
    assert len(res.json) == 1
    assert res.json["error"] == "Institution does not exist"


def test_institutions_patch_wrong_user(client):
    test_institutions_post2(client)  # create institution

    headers = {"authToken": TOKEN_1, "id": 5, "name": "NewExampleInstitution", "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client.patch('/api/institutions', headers=headers)
    assert res._status_code == 403
    assert len(res.json) == 1
    assert res.json["error"] == "no permission"


def test_institutions_patch_bad_user(client):
    test_institutions_post2(client)  # create institution

    headers = {"authToken": TOKEN_3, "id": 5, "name": "NewExampleInstitution", "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client.patch('/api/institutions', headers=headers)
    assert res._status_code == 404
