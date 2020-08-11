"""Tests for resource donations."""
from backend.smart_contracts.web3 import WEB3
from tests.test_blockstackauth import TOKEN_1, TOKEN_2, TOKEN_3
from tests.test_resource_user import test_user_post


def test_donations_get(client):
    res = client.get('/api/donations')
    assert res._status_code == 200
    assert len(res.json) == 4

    assert res.json[0]["id"] == 1
    assert res.json[0]["amount"] == WEB3.toWei(0.03, 'ether')
    assert res.json[0]["userid"] == 1
    assert res.json[0]["milestoneid"] == 1
    assert res.json[0]["projectid"] == 1
    assert res.json[0]["projectname"] == "Computer malt Bild"

    assert res.json[1]["id"] == 2
    assert res.json[1]["amount"] == WEB3.toWei(0.02, 'ether')
    assert res.json[1]["userid"] == 2
    assert res.json[1]["milestoneid"] == 2
    assert res.json[1]["projectid"] == 1
    assert res.json[1]["projectname"] == "Computer malt Bild"

    assert res.json[2]["id"] == 3
    assert res.json[2]["amount"] == WEB3.toWei(0.01, 'ether')
    assert res.json[2]["userid"] == 3
    assert res.json[2]["milestoneid"] == 3
    assert res.json[2]["projectid"] == 1
    assert res.json[2]["projectname"] == "Computer malt Bild"

    assert res.json[3]["id"] == 4
    assert res.json[3]["amount"] == WEB3.toWei(0.04, 'ether')
    assert res.json[3]["userid"] == 4
    assert res.json[3]["milestoneid"] == 4
    assert res.json[3]["projectid"] == 2
    assert res.json[3]["projectname"] == "Rangaroek verteidigen"


def test_donations_get_w_id(client):
    res = client.get('/api/donations?id=4')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 4
    assert res.json[0]["amount"] == WEB3.toWei(0.04, 'ether')
    assert res.json[0]["userid"] == 4
    assert res.json[0]["milestoneid"] == 4
    assert res.json[0]["projectid"] == 2
    assert res.json[0]["projectname"] == "Rangaroek verteidigen"


def test_donations_get_w_bad_id(client):
    res = client.get('/api/donations?id=' + '1'*200)
    assert res._status_code == 200
    assert len(res.json) == 0


def test_donations_get_w_minamount(client):
    res = client.get('/api/donations?minamount=40000000000000000')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 4
    assert res.json[0]["amount"] == WEB3.toWei(0.04, 'ether')
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
    res = client.get('/api/donations?maxamount=10000000000000000')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 3
    assert res.json[0]["amount"] == WEB3.toWei(0.01, 'ether')
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
    assert res.json[0]["amount"] == WEB3.toWei(0.04, 'ether')
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
    assert res.json[0]["amount"] == WEB3.toWei(0.03, 'ether')
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
    assert res.json[0]["amount"] == WEB3.toWei(0.04, 'ether')
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
    headers = {"authToken": TOKEN_2, "idproject": 1, "amount": int(WEB3.toWei(0.02, 'ether')), "voteEnabled": 1}
    res = client_w_eth.post('/api/donations', headers=headers)

    assert res._status_code == 201
    assert len(res.json) == 1

    assert res.json["status"] == "Spende wurde verbucht"

    res = client_w_eth.get('/api/donations?iduser=7')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["amount"] == int(WEB3.toWei(0.02, 'ether'))
    assert res.json[0]["userid"] == 7
    assert res.json[0]["milestoneid"] == 1


def test_donations_post_balance(client):
    headers = {"authToken": TOKEN_2, "idproject": 1, "amount": int(WEB3.toWei(0.02, 'ether')), "voteEnabled": 1}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code in [400, 406]
    assert "balance" in res.json["error"]


def test_donations_post2(client_w_eth):
    test_user_post(client_w_eth)
    res = client_w_eth.get('/api/users?username=sw2020testuser1337.id.blockstack')
    assert res._status_code == 200

    WEB3.eth.sendTransaction({'from': WEB3.eth.accounts[9],
                              'to': res.json[0]["publickey"],
                              'value': 1 * 10 ** 18})

    headers = {"authToken": TOKEN_3, "idproject": 1, "amount": int(WEB3.toWei(0.02, 'ether')), "voteEnabled": 1}
    res = client_w_eth.post('/api/donations', headers=headers)

    assert res._status_code == 201
    assert len(res.json) == 1

    assert res.json["status"] == "Spende wurde verbucht"

    res = client_w_eth.get('/api/donations?iduser=8')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 5
    assert res.json[0]["amount"] == int(WEB3.toWei(0.02, 'ether'))
    assert res.json[0]["userid"] == 8
    assert res.json[0]["milestoneid"] == 1


def test_donations_post_multiple(client_w_eth):
    test_user_post(client_w_eth)
    res = client_w_eth.get('/api/users?username=sw2020testuser1337.id.blockstack')
    assert res._status_code == 200

    WEB3.eth.sendTransaction({'from': WEB3.eth.accounts[9],
                              'to': res.json[0]["publickey"],
                              'value': 1 * 10 ** 18})

    headers = {"authToken": TOKEN_3, "idproject": 1, "amount": int(WEB3.toWei(0.02, 'ether')), "voteEnabled": 1}
    res = client_w_eth.post('/api/donations', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1

    res = client_w_eth.post('/api/donations', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1

    res = client_w_eth.post('/api/donations', headers=headers)
    assert res._status_code == 201
    assert len(res.json) == 1

    assert res.json["status"] == "Spende wurde verbucht"

    res = client_w_eth.get('/api/donations?iduser=8')
    assert res._status_code == 200
    assert len(res.json) == 3

    assert res.json[0]["id"] == 5
    assert res.json[0]["amount"] == int(WEB3.toWei(0.02, 'ether'))
    assert res.json[0]["userid"] == 8
    assert res.json[0]["milestoneid"] == 1

    assert res.json[1]["id"] == 6
    assert res.json[1]["amount"] == int(WEB3.toWei(0.02, 'ether'))
    assert res.json[1]["userid"] == 8
    assert res.json[1]["milestoneid"] == 1

    assert res.json[2]["id"] == 7
    assert res.json[2]["amount"] == int(WEB3.toWei(0.02, 'ether'))
    assert res.json[2]["userid"] == 8
    assert res.json[2]["milestoneid"] == 1


def test_donations_post_w_nonexistant_milestone(client):
    headers = {"authToken": TOKEN_1, "idproject": 1337, "amount": 1337, "voteEnabled": 0}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1

    assert res.json["error"] == "Project not found"


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
    headers = {"authToken": TOKEN_1, "idproject": "test", "amount": 1337, "voteEnabled": 0}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1

    assert res.json["error"] == "bad argument"


def test_donations_post_bad_param2(client):
    headers = {"authToken": TOKEN_1, "idproject": 1, "amount": -1337, "voteEnabled": 0}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1

    assert res.json["error"] == "amount cant be 0 or less"


def test_donations_post_wo_auth(client):
    headers = {"idproject": 1337, "amount": 1337, "etherAccountKey": "89354joiternjkfsdhiu4378z"}
    res = client.post('/api/donations', headers=headers)

    assert res._status_code == 401


def test_donations_vote(client_w_eth):
    test_donations_post(client_w_eth)

    headers = {"authToken": TOKEN_2, "id": 5, "vote": 1}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code == 200
    assert len(res.json) == 1
    assert res.json["status"] == "ok"


def test_donations_vote_balance(client_w_eth):
    test_donations_post(client_w_eth)
    # spend all money
    signed_tx = WEB3.eth.account.signTransaction({'from': '0x7Dca2Ba711f089C608ABe8C6F59Fe7B5F84fced8',
                                                  'nonce': WEB3.eth.getTransactionCount('0x7Dca2Ba711f089C608ABe8C6F59Fe7B5F84fced8'),
                                                  'to': WEB3.eth.defaultAccount,  # sw2020testuser2.id.blockstack
                                                  'value': WEB3.eth.getBalance('0x7Dca2Ba711f089C608ABe8C6F59Fe7B5F84fced8') - WEB3.eth.gasPrice * 21000,
                                                  'gasPrice': WEB3.eth.gasPrice,
                                                  'gas': 21000},
                                                 b'\x02P\x13\x96\xdc\xae\x86\x86\xff\x86\x83)Hj\xf1\x1c\x94\xc7?\xabj'
                                                 b'\xda\x93\t\xc0\xe8\xe4\t\xde\xd1M\xaf')
    WEB3.eth.waitForTransactionReceipt(WEB3.eth.sendRawTransaction(signed_tx.rawTransaction))

    headers = {"authToken": TOKEN_2, "id": 5, "vote": 1}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code in [400, 406]
    assert "balance" in res.json["error"]


def test_donations_vote2(client_w_eth):
    headers = {"authToken": TOKEN_2, "idproject": 1, "amount": int(WEB3.toWei(0.02, 'ether')), "voteEnabled": 1}
    res = client_w_eth.post('/api/donations', headers=headers)
    assert res._status_code == 201
    headers = {"authToken": TOKEN_2, "idproject": 1, "amount": int(WEB3.toWei(0.02, 'ether')), "voteEnabled": 1}
    res = client_w_eth.post('/api/donations', headers=headers)
    assert res._status_code == 201

    headers = {"authToken": TOKEN_2, "id": 5, "vote": 1}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code == 200
    assert len(res.json) == 1
    assert res.json["status"] == "ok"

    headers = {"authToken": TOKEN_2, "id": 6, "vote": 0}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "already voted"


def test_donations_vote_donate_voteagain(client_w_eth):
    headers = {"authToken": TOKEN_2, "idproject": 1, "amount": int(WEB3.toWei(0.02, 'ether')), "voteEnabled": 1}
    res = client_w_eth.post('/api/donations', headers=headers)
    assert res._status_code == 201

    headers = {"authToken": TOKEN_2, "id": 5, "vote": 1}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code == 200
    assert len(res.json) == 1
    assert res.json["status"] == "ok"

    headers = {"authToken": TOKEN_2, "idproject": 1, "amount": int(WEB3.toWei(0.02, 'ether')), "voteEnabled": 1}
    res = client_w_eth.post('/api/donations', headers=headers)
    assert res._status_code == 201

    headers = {"authToken": TOKEN_2, "id": 6, "vote": 0}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "already voted"


def test_donations_vote_double(client_w_eth):
    test_donations_post(client_w_eth)

    headers = {"authToken": TOKEN_2, "id": 5, "vote": 1}
    res = client_w_eth.post('/api/donations/vote', headers=headers)
    assert res._status_code == 200
    assert len(res.json) == 1
    assert res.json["status"] == "ok"

    res = client_w_eth.post('/api/donations/vote', headers=headers)
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "already voted"


def test_donations_vote_missing(client_w_eth):
    headers = {"authToken": TOKEN_2, "vote": 1}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "Missing parameter"


def test_donations_vote_missing2(client_w_eth):
    headers = {"authToken": TOKEN_2, "id": 3}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "Missing parameter"


def test_donations_vote_bad_param(client_w_eth):
    headers = {"authToken": TOKEN_2, "id": 3, "vote": "test"}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "bad argument"


def test_donations_vote_bad_id(client_w_eth):
    headers = {"authToken": TOKEN_2, "id": 1337, "vote": 1}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code == 404
    assert len(res.json) == 1
    assert res.json["error"] == "donation not found"


def test_donations_vote_didnt_register(client_w_eth):
    headers = {"authToken": TOKEN_2, "id": 4, "vote": 1}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "didn't register to vote"


def test_donations_vote_unauthorized(client_w_eth):
    headers = {"authToken": TOKEN_2, "id": 3, "vote": 1}
    res = client_w_eth.post('/api/donations/vote', headers=headers)

    assert res._status_code == 401
    assert len(res.json) == 1
    assert res.json["error"] == "unauthorized user"


