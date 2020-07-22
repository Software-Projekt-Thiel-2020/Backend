"""Tests for resource donations."""
from tests.test_blockstackauth import TOKEN_1, TOKEN_2


def test_donations_get(client):
    res = client.get('/api/donations')
    assert res._status_code == 200
    assert len(res.json) == 4

    assert res.json[0]["id"] == 1
    assert res.json[0]["amount"] == 300
    assert res.json[0]["userid"] == 1
    assert res.json[0]["milestoneid"] == 1
    assert res.json[0]["projectid"] == 1
    assert res.json[0]["projectname"] == "Computer malt Bild"

    assert res.json[1]["id"] == 2
    assert res.json[1]["amount"] == 200
    assert res.json[1]["userid"] == 2
    assert res.json[1]["milestoneid"] == 2
    assert res.json[1]["projectid"] == 1
    assert res.json[1]["projectname"] == "Computer malt Bild"

    assert res.json[2]["id"] == 3
    assert res.json[2]["amount"] == 100
    assert res.json[2]["userid"] == 3
    assert res.json[2]["milestoneid"] == 3
    assert res.json[2]["projectid"] == 1
    assert res.json[2]["projectname"] == "Computer malt Bild"

    assert res.json[3]["id"] == 4
    assert res.json[3]["amount"] == 400
    assert res.json[3]["userid"] == 4
    assert res.json[3]["milestoneid"] == 4
    assert res.json[3]["projectid"] == 2
    assert res.json[3]["projectname"] == "Rangaroek verteidigen"


def test_donations_get_w_id(client):
    res = client.get('/api/donations?id=4')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 4
    assert res.json[0]["amount"] == 400
    assert res.json[0]["userid"] == 4
    assert res.json[0]["milestoneid"] == 4
    assert res.json[0]["projectid"] == 2
    assert res.json[0]["projectname"] == "Rangaroek verteidigen"


def test_donations_get_w_bad_id(client):
    res = client.get('/api/donations?id=' + '1'*200)
    assert res._status_code == 200
    assert len(res.json) == 0


def test_donations_get_w_minamount(client):
    res = client.get('/api/donations?minamount=400')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 4
    assert res.json[0]["amount"] == 400
    assert res.json[0]["userid"] == 4
    assert res.json[0]["milestoneid"] == 4
    assert res.json[0]["projectid"] == 2
    assert res.json[0]["projectname"] == "Rangaroek verteidigen"


def test_donations_get_w_minamount_toobig(client):
    res = client.get('/api/donations?minamount=' + "1" * 400)
    assert res._status_code == 200
    assert len(res.json) == 0


def test_donations_get_w_minamount_bad_value(client):
    res = client.get('/api/donations?minamount=abcdefg')
    assert res._status_code == 400


def test_donations_get_w_maxamount(client):
    res = client.get('/api/donations?maxamount=100')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 3
    assert res.json[0]["amount"] == 100
    assert res.json[0]["userid"] == 3
    assert res.json[0]["milestoneid"] == 3
    assert res.json[0]["projectid"] == 1
    assert res.json[0]["projectname"] == "Computer malt Bild"


def test_donations_get_w_maxamount_toosmall(client):
    res = client.get('/api/donations?maxamount=0')
    assert res._status_code == 200
    assert len(res.json) == 0


def test_donations_get_w_maxamount_toosmall2(client):
    res = client.get('/api/donations?maxamount=-1000')
    assert res._status_code == 200
    assert len(res.json) == 0


def test_donations_get_w_maxamount_bad_value(client):
    res = client.get('/api/donations?maxamount=abcdefg')
    assert res._status_code == 400


def test_donations_get_w_user(client):
    res = client.get('/api/donations?iduser=4')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 4
    assert res.json[0]["amount"] == 400
    assert res.json[0]["userid"] == 4
    assert res.json[0]["milestoneid"] == 4
    assert res.json[0]["projectid"] == 2
    assert res.json[0]["projectname"] == "Rangaroek verteidigen"


def test_donations_get_w_user_nonexistant(client):
    res = client.get('/api/donations?iduser=' + "1" * 400)
    assert res._status_code == 200
    assert len(res.json) == 0


def test_donations_get_w_user_bad_value(client):
    res = client.get('/api/donations?iduser=abcdefg')
    assert res._status_code == 400


def test_donations_get_w_milestone(client):
    res = client.get('/api/donations?idmilestone=1')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["amount"] == 300
    assert res.json[0]["userid"] == 1
    assert res.json[0]["milestoneid"] == 1
    assert res.json[0]["projectid"] == 1
    assert res.json[0]["projectname"] == "Computer malt Bild"


def test_donations_get_w_milestone_nonexistant(client):
    res = client.get('/api/donations?idmilestone=' + "1" * 400)
    assert res._status_code == 200
    assert len(res.json) == 0


def test_donations_get_w_milestone_bad_value(client):
    res = client.get('/api/donations?idmilestone=abcdefg')
    assert res._status_code == 400


def test_donations_get_w_project(client):
    res = client.get('/api/donations?idproject=2')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 4
    assert res.json[0]["amount"] == 400
    assert res.json[0]["userid"] == 4
    assert res.json[0]["milestoneid"] == 4
    assert res.json[0]["projectid"] == 2
    assert res.json[0]["projectname"] == "Rangaroek verteidigen"


def test_donations_get_w_project2(client):
    res = client.get('/api/donations?idproject=3')
    assert res._status_code == 200
    assert len(res.json) == 0


def test_donations_get_w_project_nonexistant(client):
    res = client.get('/api/donations?idproject=' + "1" * 400)
    assert res._status_code == 200
    assert len(res.json) == 0


def test_donations_get_w_project_bad_value(client):
    res = client.get('/api/donations?idproject=abcdefg')
    assert res._status_code == 400


def test_donations_post(client_w_eth):
    headers = {"authToken": TOKEN_1, "idmilestone": 1, "amount": 1337, "voteEnabled": 1}
    res = client_w_eth.post('/api/donations', headers=headers)

    assert res._status_code == 201
    assert len(res.json) == 1

    assert res.json["status"] == "Spende wurde verbucht"

    res = client_w_eth.get('/api/donations?iduser=6')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["amount"] == 1337
    assert res.json[0]["userid"] == 6
    assert res.json[0]["milestoneid"] == 1


def test_donations_post_w_nonexistant_milestone(client):
    headers = {"authToken": TOKEN_1, "idmilestone": 1337, "amount": 1337, "voteEnabled": 0}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1

    assert res.json["error"] == "Milestone not found"


def test_donations_post_missing_param1(client):
    headers = {"authToken": TOKEN_1, "amount": 1337, "etherAccountKey": "89354joiternjkfsdhiu4378z"}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1

    assert res.json["error"] == "Missing parameter"


def test_donations_post_missing_param2(client):
    headers = {"authToken": TOKEN_1, "idmilestone": 1337, "etherAccountKey": "89354joiternjkfsdhiu4378z"}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1

    assert res.json["error"] == "Missing parameter"


def test_donations_post_missing_param3(client):
    headers = {"authToken": TOKEN_1, "idmilestone": 1337, "amount": 1337}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1

    assert res.json["error"] == "Missing parameter"


def test_donations_post_bad_param(client):
    headers = {"authToken": TOKEN_1, "idmilestone": "test", "amount": 1337, "voteEnabled": 0}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1

    assert res.json["error"] == "bad argument"


def test_donations_post_bad_param2(client):
    headers = {"authToken": TOKEN_1, "idmilestone": 1, "amount": -1337, "voteEnabled": 0}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1

    assert res.json["error"] == "amount cant be 0 or less"


def test_donations_post_wo_auth(client):
    headers = {"idmilestone": 1337, "amount": 1337, "etherAccountKey": "89354joiternjkfsdhiu4378z"}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code == 401


