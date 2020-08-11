"""Tests for resource institutions."""
from backend.smart_contracts.web3 import WEB3
from tests.test_blockstackauth import TOKEN_1, TOKEN_2, TOKEN_3
from base64 import b64encode

ACCOUNTS = list(WEB3.eth.accounts)


def test_institutions_get(client):
    res = client.get('/api/institutions')
    assert res._status_code == 200
    assert len(res.json) == 4

    assert res.json[0]["id"] == 1
    assert res.json[0]["name"] == "MSGraphic"
    assert res.json[0]["webpage"] == "http://www.msgraphic.com"
    assert res.json[0]["address"] == "Address1"

    assert res.json[1]["id"] == 2
    assert res.json[1]["name"] == "SWP"
    assert res.json[1]["webpage"] == "http://www.swp.com"
    assert res.json[1]["address"] == "Address2"

    assert res.json[2]["id"] == 3
    assert res.json[2]["name"] == "Asgard Inc."
    assert res.json[2]["webpage"] == "http://www.asgard.as"
    assert res.json[2]["address"] == "Address3"

    assert res.json[3]["id"] == 4
    assert res.json[3]["name"] == "Blackhole"
    assert res.json[3]["webpage"] == "http://127.0.0.1"
    assert res.json[3]["address"] == "Address4"


def test_institutions_get_id(client):
    res = client.get('/api/institutions?id=1')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["name"] == "MSGraphic"
    assert res.json[0]["webpage"] == "http://www.msgraphic.com"
    assert res.json[0]["address"] == "Address1"


def test_institutions_get_username(client):
    res = client.get('/api/institutions?username=sw2020testuser1.id.blockstack')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["name"] == "MSGraphic"
    assert res.json[0]["webpage"] == "http://www.msgraphic.com"
    assert res.json[0]["address"] == "Address1"


def test_institutions_get_name(client):
    res = client.get('/api/institutions?name=Graphic')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["name"] == "MSGraphic"
    assert res.json[0]["webpage"] == "http://www.msgraphic.com"
    assert res.json[0]["address"] == "Address1"


def test_institutions_get_hasvouchers(client):
    res = client.get('/api/institutions?has_vouchers=1')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["name"] == "MSGraphic"
    assert res.json[0]["webpage"] == "http://www.msgraphic.com"
    assert res.json[0]["address"] == "Address1"


def test_institutions_get_hasvouchers2(client):
    res = client.get('/api/institutions?has_vouchers=0')
    assert res._status_code == 200
    assert len(res.json) == 3

    assert res.json[0]["id"] == 2
    assert res.json[0]["name"] == "SWP"
    assert res.json[0]["webpage"] == "http://www.swp.com"
    assert res.json[0]["address"] == "Address2"

    assert res.json[1]["id"] == 3
    assert res.json[1]["name"] == "Asgard Inc."
    assert res.json[1]["webpage"] == "http://www.asgard.as"
    assert res.json[1]["address"] == "Address3"

    assert res.json[2]["id"] == 4
    assert res.json[2]["name"] == "Blackhole"
    assert res.json[2]["webpage"] == "http://127.0.0.1"
    assert res.json[2]["address"] == "Address4"


def test_institutions_get_geo(client):
    res = client.get('/api/institutions?radius=1&latitude=52.030228&longitude=8.532471')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["name"] == "MSGraphic"
    assert res.json[0]["webpage"] == "http://www.msgraphic.com"
    assert res.json[0]["address"] == "Address1"


def test_institutions_get_geo2(client):
    res = client.get('/api/institutions?radius=1200&latitude=52.030228&longitude=8.532471')
    # distance between institution 1 and 4 is ~ 1163km
    assert res._status_code == 200
    assert len(res.json) == 2

    assert res.json[0]["id"] == 1
    assert res.json[1]["id"] == 4


def test_institutions_get_geo_bad(client):
    res = client.get('/api/institutions?radius=1200')
    assert res._status_code == 400


def test_institutions_get_geo_bad2(client):
    res = client.get('/api/institutions?radius=1200&latitude=52.030228&longitude=test')
    assert res._status_code == 400
    assert res.json['error'] == "bad argument"


def test_institutions_get_bad_id(client):
    res = client.get('/api/institutions?id=1337')
    assert res._status_code == 200
    assert len(res.json) == 0


def test_institutions_get_bad_id2(client):
    res = client.get('/api/institutions?id=aaa')
    assert res._status_code == 400
    assert res.json['error'] == "bad argument"


def test_institutions_post(client_w_eth):
    headers = {"authToken": TOKEN_1, "username": "sw2020testuser2.id.blockstack", "name": "ExampleInstitution",
               "address": "Address", "description": b64encode(b"description"), "latitude": 13.37, "longitude": 42.69,
               "publickey": ACCOUNTS[2], "short": b64encode(b"sdesc")}
    res = client_w_eth.post('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde erstellt"

    res = client_w_eth.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["name"] == "ExampleInstitution"
    assert res.json[0]["webpage"] is None
    assert res.json[0]["address"] == "Address"
    assert res.json[0]["description"] == "description"
    assert res.json[0]["latitude"] == 13.37
    assert res.json[0]["short"] == "sdesc"
    assert res.json[0]["longitude"] == 42.69


def test_institutions_post2(client_w_eth):
    headers = {"authToken": TOKEN_1, "username": "sw2020testuser2.id.blockstack", "name": "ExampleInstitution",
               "address": "Address", "webpage": "https://www.example.com/", "description": b64encode(b"description"),
               "latitude": 13.37, "longitude": 42.69, "publickey": ACCOUNTS[2]}
    res = client_w_eth.post('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde erstellt"

    res = client_w_eth.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["name"] == "ExampleInstitution"
    assert res.json[0]["webpage"] == "https://www.example.com/"
    assert res.json[0]["address"] == "Address"


def test_institutions_post_bad_owner(client):
    headers = {"authToken": TOKEN_1, "username": "sw2020testuser1337.id.blockstack", "name": "ExampleInstitution",
               "address": "Address", "webpage": "https://www.example.com/", "description": b64encode(b"description"),
               "latitude": 13.37, "longitude": 42.69, "publickey": ACCOUNTS[3]}
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "username not found"


def test_institutions_post_bad_geo(client):
    headers = {"authToken": TOKEN_1, "username": "sw2020testuser2.id.blockstack", "name": "ExampleInstitution",
               "address": "Address", "webpage": "https://www.example.com/", "description": b64encode(b"description"),
               "latitude": 13.37, "longitude": "a", "publickey": ACCOUNTS[3]}
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "bad argument"


def test_institutions_post_non_support_user(client):
    headers = {"authToken": TOKEN_2, "username": "sw2020testuser2.id.blockstack", "name": "ExampleInstitution",
               "address": "Address", "webpage": "https://www.example.com/", "description": b64encode(b"description"),
               "latitude": 13.37, "longitude": 42.69, "publickey": ACCOUNTS[2]}
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
               "webpage": "NotAValidURL", "description": b64encode(b"description"), "latitude": 13.37, "longitude": 42.69,
               "publickey": ACCOUNTS[2]}
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "webpage is not a valid url"


def test_institutions_post_existing_name(client):
    headers = {"authToken": TOKEN_1, "username": "sw2020testuser2.id.blockstack", "name": "MSGraphic",
               "address": "Address", "webpage": "https://www.example.com/", "description": b64encode(b"description"),
               "latitude": 13.37, "longitude": 42.69, "publickey": ACCOUNTS[2]}
    res = client.post('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "name already exists"


def test_institutions_patch(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5, "name": "NewExampleInstitution", "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client_w_eth.patch('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde bearbeitet"

    res = client_w_eth.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["name"] == "NewExampleInstitution"
    assert res.json[0]["webpage"] == "https://www.new_example.com/"
    assert res.json[0]["address"] == "NewAddress"


def test_institutions_patch2(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5, "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client_w_eth.patch('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde bearbeitet"

    res = client_w_eth.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["name"] == "ExampleInstitution"
    assert res.json[0]["webpage"] == "https://www.new_example.com/"
    assert res.json[0]["address"] == "NewAddress"


def test_institutions_patch3(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5, "webpage": "https://www.new_example.com/"}
    res = client_w_eth.patch('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde bearbeitet"

    res = client_w_eth.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["name"] == "ExampleInstitution"
    assert res.json[0]["webpage"] == "https://www.new_example.com/"
    assert res.json[0]["address"] == "Address"


def test_institutions_patch4(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5,
               "latitude": 13.37, "longitude": 42.69}
    res = client_w_eth.patch('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde bearbeitet"

    res = client_w_eth.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["latitude"] == 13.37
    assert res.json[0]["longitude"] == 42.69


def test_institutions_patch5(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5, "description": b64encode(b"description1234")}
    res = client_w_eth.patch('/api/institutions', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1
    assert res.json["status"] == "Institution wurde bearbeitet"

    res = client_w_eth.get('/api/institutions?id=5')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["description"] == "description1234"


def test_institutions_patch_missing_id(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_2, "name": "NewExampleInstitution", "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client_w_eth.patch('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "Missing parameter"


def test_institutions_patch_bad_geo(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5,  "name": "NewExampleInstitution", "address": "NewAddress",
               "webpage": "https://www.new_example.com/", "latitude": 13.37, "longitude": "aaa"}
    res = client_w_eth.patch('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "bad argument"


def test_institutions_patch_bad_geo2(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5,  "name": "NewExampleInstitution", "address": "NewAddress",
               "webpage": "https://www.new_example.com/", "latitude": 13.37}
    res = client_w_eth.patch('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "bad geo argument"


def test_institutions_patch_name_exists(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5, "name": "MSGraphic", "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client_w_eth.patch('/api/institutions', headers=headers)
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


def test_institutions_patch_wrong_user(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_1, "id": 5, "name": "NewExampleInstitution", "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client_w_eth.patch('/api/institutions', headers=headers)
    assert res._status_code == 403
    assert len(res.json) == 1
    assert res.json["error"] == "no permission"


def test_institutions_patch_bad_user(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_3, "id": 5, "name": "NewExampleInstitution", "address": "NewAddress",
               "webpage": "https://www.new_example.com/"}
    res = client_w_eth.patch('/api/institutions', headers=headers)
    assert res._status_code == 404


def test_institutions_patch_long_name(client_w_eth):
    test_institutions_post2(client_w_eth)  # create institution

    headers = {"authToken": TOKEN_2, "id": 5,
               "name": "thisnameistoofuckinglonglikeseriouslywhoreadsthisnicolascageistruelythebestactoralivefollowedbykevinspaceybutthepointisthatidonthavebockanymoreandibringmyvomitbagoutsidesurturisthebringerflamesnadasgardwillgodownwhenirisesinthetimesofragnarokodinisinfearfuckoff"}
    res = client_w_eth.patch('/api/institutions', headers=headers)
    assert res._status_code == 400
    assert res.json["error"] == "bad name argument"

