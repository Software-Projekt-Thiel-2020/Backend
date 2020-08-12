"""Tests for resource projects."""
import json

from backend.smart_contracts.web3 import WEB3
from .test_blockstackauth import TOKEN_1, TOKEN_2

from base64 import b64encode


def test_projects_get(client):
    """get without parameters."""
    res = client.get('/api/projects')
    assert res._status_code == 200
    assert len(res.json) == 3

    assert res.json[0]["id"] == 1
    assert res.json[0]["idinstitution"] == 1
    assert res.json[0]["name"] == "Computer malt Bild"
    assert res.json[0]["webpage"] == "http://www.cmb.de"

    assert res.json[1]["id"] == 2
    assert res.json[1]["idinstitution"] == 3
    assert res.json[1]["name"] == "Rangaroek verteidigen"
    assert res.json[1]["webpage"] == "http://www.asgard.as"

    assert res.json[2]["id"] == 3
    assert res.json[2]["idinstitution"] == 3
    assert res.json[2]["name"] == "Softwareprojekt 2020"
    assert res.json[2]["webpage"] == "http://www.swp.de"


def test_projects_get_name(client):
    """get without parameters."""
    res = client.get('/api/projects?name=puter')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["idinstitution"] == 1
    assert res.json[0]["name"] == "Computer malt Bild"
    assert res.json[0]["webpage"] == "http://www.cmb.de"


def test_projects_get_userid(client):
    """get without parameters."""
    res = client.get('/api/projects?username=sw2020testuser1.id.blockstack')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["idinstitution"] == 1
    assert res.json[0]["name"] == "Computer malt Bild"
    assert res.json[0]["webpage"] == "http://www.cmb.de"


def test_projects_get_geo(client):
    """get without parameters."""
    res = client.get('/api/projects?radius=1&latitude=52.030228&longitude=8.532471')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["idinstitution"] == 1
    assert res.json[0]["name"] == "Computer malt Bild"
    assert res.json[0]["webpage"] == "http://www.cmb.de"


def test_projects_get_bad_geo(client):
    """get without parameters."""
    res = client.get('/api/projects?radius=1&latitude=52.030228&longitude=aaa')
    assert res._status_code == 400
    assert res.json["error"] == "bad geo argument"


def test_projects_get_w_institution(client):
    """get with id_institution."""
    res = client.get('/api/projects?idinstitution=3')
    assert res._status_code == 200
    assert len(res.json) == 2

    assert res.json[0]["id"] == 2
    assert res.json[0]["idinstitution"] == 3
    assert res.json[0]["name"] == "Rangaroek verteidigen"
    assert res.json[0]["webpage"] == "http://www.asgard.as"

    assert res.json[1]["id"] == 3
    assert res.json[1]["idinstitution"] == 3
    assert res.json[1]["name"] == "Softwareprojekt 2020"
    assert res.json[1]["webpage"] == "http://www.swp.de"


def test_projects_get_w_id(client):
    """get with id_institution."""
    res = client.get('/api/projects?id=2')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 2
    assert res.json[0]["idinstitution"] == 3
    assert res.json[0]["name"] == "Rangaroek verteidigen"
    assert res.json[0]["webpage"] == "http://www.asgard.as"


def test_projects_get_w_bad_id(client):
    """get with id_institution."""
    res = client.get('/api/projects?id=' + '1'*200)
    assert res._status_code == 200
    assert len(res.json) == 0


def test_projects_get_w_non_existant_institution(client):
    """get with non existant id_institution."""
    res = client.get('/api/projects?idinstitution=1337')
    assert res._status_code == 200
    assert len(res.json) == 0


def test_projects_get_w_bad_institution_value(client):
    """get with bad value as id_institution."""
    res = client.get('/api/projects?idinstitution=abcdefg')
    assert res._status_code == 400
    assert len(res.json) == 1


def test_projects_get_w_very_big_institution_value(client):
    """get with VERYBIGINT as value of id_institution."""
    res = client.get(
        '/api/projects?idinstitution=' + "1" * 200)
    assert res._status_code == 200
    assert len(res.json) == 0


def test_projects_get_w_nonexistant_param(client):
    """get with non existant parameter."""
    res = client.get('/api/projects?NonExistantParam=3000')
    assert res._status_code == 200
    assert len(res.json) == 3


def test_projects_get_w_existant_unexpected_param(client):
    """get with existant but unexpected parameter."""
    res = client.get('/api/projects?nameProject=Computer%20malt%20Bild')
    assert res._status_code == 200
    assert len(res.json) == 3


def test_projects_get_w_existant_unexpected_param2(client):
    """get with existant but unexpected param and bad value."""
    res = client.get('/api/projects?firstnameUser=NonExistantUser')
    assert res._status_code == 200
    assert len(res.json) == 3


def test_projects_id_get_existant_param(client):
    """get for project id with existant id."""
    res = client.get('/api/projects/1')
    assert res._status_code == 200
    assert len(res.json) == 14

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["webpage"] == "http://www.cmb.de"
    assert res.json["address"] == "Address1"
    assert res.json["until"] == 1693094933
    assert res.json["goal"] == WEB3.toWei(1, 'ether')

    assert len(res.json["milestones"]) == 4
    assert res.json["milestones"][0]["id"] == 1
    assert res.json["milestones"][0]["idProjekt"] == 1
    assert res.json["milestones"][0]["goal"] == WEB3.toWei(0.1, 'ether')
    assert res.json["milestones"][0]["until"] == 1693094933
    assert res.json["milestones"][0]["totalDonated"] == WEB3.toWei(0.03, 'ether')
    assert res.json["milestones"][0]["positiveVotes"] == 1
    assert res.json["milestones"][0]["negativeVotes"] == 0

    assert res.json["milestones"][1]["id"] == 2
    assert res.json["milestones"][1]["idProjekt"] == 1
    assert res.json["milestones"][1]["goal"] == WEB3.toWei(0.2, 'ether')
    assert res.json["milestones"][1]["until"] == 1693094933
    assert res.json["milestones"][1]["totalDonated"] == WEB3.toWei(0.02, 'ether')
    assert res.json["milestones"][1]["positiveVotes"] == 0
    assert res.json["milestones"][1]["negativeVotes"] == 0

    assert res.json["milestones"][2]["id"] == 3
    assert res.json["milestones"][2]["idProjekt"] == 1
    assert res.json["milestones"][2]["goal"] == WEB3.toWei(0.3, 'ether')
    assert res.json["milestones"][2]["until"] == 1693094933
    assert res.json["milestones"][2]["totalDonated"] == WEB3.toWei(0.01, 'ether')
    assert res.json["milestones"][2]["positiveVotes"] == 0
    assert res.json["milestones"][2]["negativeVotes"] == 1

    assert res.json["milestones"][3]["id"] == 7
    assert res.json["milestones"][3]["idProjekt"] == 1
    assert res.json["milestones"][3]["goal"] == WEB3.toWei(0.5, 'ether')
    assert res.json["milestones"][3]["until"] == 1693094933
    assert res.json["milestones"][3]["totalDonated"] == 0
    assert res.json["milestones"][3]["positiveVotes"] == 0
    assert res.json["milestones"][3]["negativeVotes"] == 0

    assert res.json['totalDonated'] == \
        res.json["milestones"][0]["totalDonated"] + \
        res.json["milestones"][1]["totalDonated"] + \
        res.json["milestones"][2]["totalDonated"] + \
        res.json["milestones"][3]["totalDonated"]


def test_projects_id_get_nonexistant_param(client):
    """get for project id with invalid id"""
    res = client.get('/api/projects/1337')
    assert res._status_code == 404
    assert len(res.json) == 0


def test_projects_id_get_bad_value(client):
    """get for project id with bad value"""
    res = client.get('/api/projects/abcdefg')
    assert res._status_code == 400
    assert len(res.json) == 1


def test_projects_id_get_big_value(client):
    """get for project id with very big int as id"""
    res = client.get('/api/projects/' + "1" * 200)
    assert res._status_code == 404
    assert len(res.json) == 0


def test_projects_post_wo_params(client):
    res = client.post('/api/projects')
    assert res._status_code == 401


def test_projects_post_w_auth_wo_params(client):
    res = client.post('/api/projects', headers={"authToken": TOKEN_1})
    assert res._status_code == 403
    assert res.json["error"] == "Missing parameter"


def test_projects_post_w_auth_bad_params(client):
    milestones = [
        {"name": "goal_1", "goal": 100, "requiredVotes": 1337, "until": 1693094933},
        {"name": "goal_2", "goal": 500, "requiredVotes": 42, "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_1, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1792094933,
               "milestones": json.dumps(milestones), "idInstitution": "abc", "description": b64encode(b"test description"), "short": b64encode(b"sdesc")}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 400
    assert res.json["error"] == "bad argument"


def test_projects_post_w_no_permission(client):
    milestones = [
        {"name": "goal_1", "goal": 100, "requiredVotes": 1337, "until": 1693094933},
        {"name": "goal_2", "goal": 500, "requiredVotes": 42, "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_1, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1792094933,
               "milestones": json.dumps(milestones), "idInstitution": 4, "description": b64encode(b"test description"), "short": b64encode(b"sdesc")}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 403
    assert res.json["error"] == "User has no permission to create projects for this institution"


def test_projects_post_required_params_no_milestone(client_w_eth):
    headers = {"authToken": TOKEN_2, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1892094933,
               "idInstitution": 4, "description": b64encode(b"test description"), "short": b64encode(b"sdesc")}
    res = client_w_eth.post('/api/projects', headers=headers)
    assert res._status_code == 403
    assert res.json["error"] == "Missing milestone"


def test_projects_post_w_bad_milestones(client):
    headers = {"authToken": TOKEN_2, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1792094933,
               "milestones": "dennis", "idInstitution": 4, "description": b64encode(b"test description"), "short": b64encode(b"sdesc")}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 400
    assert res.json["error"] == "invalid json"


def test_projects_post_balance(client):
    milestones = [
        {"name": "goal_1", "goal": 100, "requiredVotes": 1337, "until": 1693094933},
        {"name": "goal_2", "goal": 500, "requiredVotes": 42, "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_2, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1792094933,
               "milestones": json.dumps(milestones), "idInstitution": 4, "description": b64encode(b"test description"),
               "short": b64encode(b"sdesc")}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code in [400, 406]
    assert "balance" in res.json["error"]


def test_projects_post_w_milestones(client_w_eth):
    milestones = [
        {"name": "goal_1", "goal": 100, "requiredVotes": 1337, "until": 1693094933},
        {"name": "goal_2", "goal": 500, "requiredVotes": 42, "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_2, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1792094933,
               "milestones": json.dumps(milestones), "idInstitution": 4, "description": b64encode(b"test description"),
               "short": b64encode(b"sdesc")}
    res = client_w_eth.post('/api/projects', headers=headers)
    assert res._status_code == 201
    assert res.json["status"] == "ok"

    res = client_w_eth.get('/api/projects/4')
    assert res._status_code == 200

    assert res.json["id"] == 4
    assert res.json["idinstitution"] == 4
    assert res.json["name"] == headers["name"]
    assert res.json["webpage"] is None
    assert res.json["address"] == "Address4"
    assert res.json["until"] == 1792094933

    assert len(res.json["milestones"]) == 2
    assert res.json["milestones"][0]["id"] == 8
    assert res.json["milestones"][0]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][0]["goal"] == milestones[0]["goal"]
    assert res.json["milestones"][0]["until"] == milestones[0]["until"]

    assert res.json["milestones"][1]["id"] == 9
    assert res.json["milestones"][1]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][1]["goal"] == milestones[1]["goal"]
    assert res.json["milestones"][1]["until"] == milestones[1]["until"]


def test_projects_post_balance(client):
    milestones = [
        {"name": "goal_1", "goal": 100, "requiredVotes": 1337, "until": 1693094933},
        {"name": "goal_2", "goal": 500, "requiredVotes": 42, "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_2, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1792094933,
               "milestones": json.dumps(milestones), "idInstitution": 4, "description": b64encode(b"test description"),
               "short": b64encode(b"sdesc")}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code in [400, 406]
    assert "balance" in res.json["error"]


def test_projects_post_w_webpage(client_w_eth):
    milestones = [
        {"name": "goal_1", "goal": 100, "requiredVotes": 1337, "until": 1693094933},
        {"name": "goal_2", "goal": 500, "requiredVotes": 42, "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_2, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1792094933,
               "milestones": json.dumps(milestones), "webpage": "http://www.example.com", "idInstitution": 4, "description": b64encode(b"test description"),
               "short": b64encode(b"sdesc")}
    res = client_w_eth.post('/api/projects', headers=headers)
    assert res._status_code == 201
    assert res.json["status"] == "ok"

    res = client_w_eth.get('/api/projects/4')
    assert res._status_code == 200

    assert res.json["id"] == 4
    assert res.json["idinstitution"] == 4
    assert res.json["name"] == headers["name"]
    assert res.json["webpage"] == headers["webpage"]
    assert res.json["address"] == "Address4"
    assert res.json["until"] == 1792094933

    assert len(res.json["milestones"]) == 2
    assert res.json["milestones"][0]["id"] == 8
    assert res.json["milestones"][0]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][0]["goal"] == milestones[0]["goal"]
    assert res.json["milestones"][0]["until"] == milestones[0]["until"]

    assert res.json["milestones"][1]["id"] == 9
    assert res.json["milestones"][1]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][1]["goal"] == milestones[1]["goal"]
    assert res.json["milestones"][1]["until"] == milestones[1]["until"]


def test_projects_post_w_bad_webpage(client):
    milestones = [
        {"name": "goal_1", "goal": 100, "requiredVotes": 1337, "until": 1693094933},
        {"name": "goal_2", "goal": 500, "requiredVotes": 42, "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_1, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1592094933,
               "milestones": json.dumps(milestones), "webpage": "notaurl#22*3\\asdf", "idInstitution": 4, "description": b64encode(b"test description"),
               "short": b64encode(b"sdesc")}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 400
    assert res.json["error"] == "webpage is not a valid url"


def test_projects_post_w_institution(client_w_eth):
    milestones = [
        {"name": "goal_1", "goal": 100, "requiredVotes": 1337, "until": 1693094933},
        {"name": "goal_2", "goal": 500, "requiredVotes": 42, "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_2, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1792094933,
               "milestones": json.dumps(milestones), "idInstitution": 4, "description": b64encode(b"test description"), "short": b64encode(b"sdesc")}
    res = client_w_eth.post('/api/projects', headers=headers)
    assert res._status_code == 201
    assert res.json["status"] == "ok"

    res = client_w_eth.get('/api/projects/4')
    assert res._status_code == 200

    assert res.json["id"] == 4
    assert res.json["idinstitution"] == headers["idInstitution"]
    assert res.json["name"] == headers["name"]
    assert res.json["webpage"] is None
    assert res.json["address"] == "Address4"
    assert res.json["until"] == 1792094933

    assert len(res.json["milestones"]) == 2
    assert res.json["milestones"][0]["id"] == 8
    assert res.json["milestones"][0]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][0]["goal"] == milestones[0]["goal"]
    assert res.json["milestones"][0]["until"] == milestones[0]["until"]

    assert res.json["milestones"][1]["id"] == 9
    assert res.json["milestones"][1]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][1]["goal"] == milestones[1]["goal"]
    assert res.json["milestones"][1]["until"] == milestones[1]["until"]


def test_projects_post_w_description(client_w_eth):
    milestones = [
        {"name": "goal_1", "goal": 100, "requiredVotes": 1337, "until": 1693094933},
        {"name": "goal_2", "goal": 500, "requiredVotes": 42, "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_2, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1792094933,
               "milestones": json.dumps(milestones), "idInstitution": 4, "description": b64encode(b"test description"), "short": b64encode(b"sdesc")}
    res = client_w_eth.post('/api/projects', headers=headers)
    assert res._status_code == 201
    assert res.json["status"] == "ok"

    res = client_w_eth.get('/api/projects/4')
    assert res._status_code == 200

    assert res.json["id"] == 4
    assert res.json["idinstitution"] == headers["idInstitution"]
    assert res.json["name"] == headers["name"]
    assert res.json["webpage"] is None
    assert res.json["address"] == "Address4"
    assert res.json["until"] == 1792094933
    assert res.json["description"] == "test description"
    assert res.json["short"] == "sdesc"

    assert len(res.json["milestones"]) == 2
    assert res.json["milestones"][0]["id"] == 8
    assert res.json["milestones"][0]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][0]["goal"] == milestones[0]["goal"]
    assert res.json["milestones"][0]["until"] == milestones[0]["until"]

    assert res.json["milestones"][1]["id"] == 9
    assert res.json["milestones"][1]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][1]["goal"] == milestones[1]["goal"]
    assert res.json["milestones"][1]["until"] == milestones[1]["until"]


def test_projects_post_w_bad_until(client):
    milestones = [
        {"name": "goal_1", "goal": 100, "requiredVotes": 1337, "until": 1693094933},
        {"name": "goal_2", "goal": 500, "requiredVotes": 42, "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_2, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1092094933,
               "milestones": json.dumps(milestones), "idInstitution": 4, "description": b64encode(b"test description"), "short": b64encode(b"sdesc")}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 400
    assert res.json["error"] == 'until value is in the past'


def test_projects_post_w_bad_institution(client):
    milestones = [
        {"name": "goal_1", "goal": 100, "requiredVotes": 1337, "until": 1693094933},
        {"name": "goal_2", "goal": 500, "requiredVotes": 42, "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_1, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1592094933,
               "milestones": json.dumps(milestones), "idInstitution": 30000, "description": b64encode(b"test description"), "short": b64encode(b"sdesc")}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 400


def test_projects_patch_w_webpage(client):
    headers = {"authToken": TOKEN_1, "webpage": "http://www.example.com"}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code == 201
    assert res.json["status"] == "ok"

    res = client.get('/api/projects/1')
    assert res._status_code == 200

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["webpage"] == headers["webpage"]

    assert len(res.json["milestones"]) == 4


def test_projects_patch_w_webpage_wrong_user(client):
    headers = {"authToken": TOKEN_2, "webpage": "http://www.example.com"}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code == 403
    assert res.json["error"] == "User has no permission to create projects for this institution"

    res = client.get('/api/projects/1')
    assert res._status_code == 200

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["webpage"] == "http://www.cmb.de"

    assert len(res.json["milestones"]) == 4


def test_projects_patch_w_description(client):
    headers = {"authToken": TOKEN_1, "description": b64encode(b"description1234")}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code == 201
    assert res.json["status"] == "ok"

    res = client.get('/api/projects/1')
    assert res._status_code == 200

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["description"] == "description1234"

    assert len(res.json["milestones"]) == 4


def test_projects_patch_w_bad_webpage(client):
    headers = {"authToken": TOKEN_1, "webpage": "notvalidurl"}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code == 400
    assert res.json["error"] == "webpage is not a valid url"

    res = client.get('/api/projects/1')
    assert res._status_code == 200

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["webpage"] == "http://www.cmb.de"

    assert len(res.json["milestones"]) == 4


def test_projects_patch_wo_auth_wo_params(client):
    res = client.patch('/api/projects/1')
    assert res._status_code == 401


def test_projects_patch_w_milestones_balance(client):
    milestones = [
        {"name": "goal_1", "goal": WEB3.toWei(0.6, 'ether'), "until": 1693094933},
        {"name": "goal_2", "goal": WEB3.toWei(0.7, 'ether'), "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_1, "milestones": json.dumps(milestones), "idInstitution": 4}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code in [400, 406]
    assert "balance" in res.json["error"]


def test_projects_patch_w_milestones(client_w_eth):
    milestones = [
        {"name": "goal_1", "goal": WEB3.toWei(0.6, 'ether'), "until": 1693094933},
        {"name": "goal_2", "goal": WEB3.toWei(0.7, 'ether'), "until": 1693094933},
    ]
    headers = {"authToken": TOKEN_1, "milestones": json.dumps(milestones), "idInstitution": 4}
    res = client_w_eth.patch('/api/projects/1', headers=headers)
    assert res._status_code == 201

    assert res.json["status"] == "ok"
    res = client_w_eth.get('/api/projects/1')
    assert res._status_code == 200

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["webpage"] == "http://www.cmb.de"

    assert len(res.json["milestones"]) == 6
    assert res.json["milestones"][0]["id"] == 1
    assert res.json["milestones"][0]["idProjekt"] == 1
    assert res.json["milestones"][0]["goal"] == WEB3.toWei(0.1, 'ether')
    assert res.json["milestones"][0]["until"] == 1693094933

    assert res.json["milestones"][1]["id"] == 2
    assert res.json["milestones"][1]["idProjekt"] == 1
    assert res.json["milestones"][1]["goal"] == WEB3.toWei(0.2, 'ether')
    assert res.json["milestones"][1]["until"] == 1693094933

    assert res.json["milestones"][2]["id"] == 3
    assert res.json["milestones"][2]["idProjekt"] == 1
    assert res.json["milestones"][2]["goal"] == WEB3.toWei(0.3, 'ether')
    assert res.json["milestones"][2]["until"] == 1693094933

    assert res.json["milestones"][3]["id"] == 7
    assert res.json["milestones"][3]["idProjekt"] == 1
    assert res.json["milestones"][3]["goal"] == WEB3.toWei(0.5, 'ether')
    assert res.json["milestones"][3]["until"] == 1693094933

    assert res.json["milestones"][4]["id"] == 8
    assert res.json["milestones"][4]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][4]["goal"] == milestones[0]["goal"]
    assert res.json["milestones"][4]["until"] == milestones[0]["until"]

    assert res.json["milestones"][5]["id"] == 9
    assert res.json["milestones"][5]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][5]["goal"] == milestones[1]["goal"]
    assert res.json["milestones"][5]["until"] == milestones[1]["until"]


def test_projects_patch_wo_params(client):
    headers = {"authToken": TOKEN_1}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code == 201

    assert res.json["status"] == "ok"
    res = client.get('/api/projects/1')
    assert res._status_code == 200

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["webpage"] == "http://www.cmb.de"

    assert len(res.json["milestones"]) == 4
    assert res.json["milestones"][0]["id"] == 1
    assert res.json["milestones"][0]["idProjekt"] == 1
    assert res.json["milestones"][0]["goal"] == WEB3.toWei(0.1, 'ether')
    assert res.json["milestones"][0]["until"] == 1693094933

    assert res.json["milestones"][1]["id"] == 2
    assert res.json["milestones"][1]["idProjekt"] == 1
    assert res.json["milestones"][1]["goal"] == WEB3.toWei(0.2, 'ether')
    assert res.json["milestones"][1]["until"] == 1693094933

    assert res.json["milestones"][2]["id"] == 3
    assert res.json["milestones"][2]["idProjekt"] == 1
    assert res.json["milestones"][2]["goal"] == WEB3.toWei(0.3, 'ether')
    assert res.json["milestones"][2]["until"] == 1693094933

    assert res.json["milestones"][3]["id"] == 7
    assert res.json["milestones"][3]["idProjekt"] == 1
    assert res.json["milestones"][3]["goal"] == WEB3.toWei(0.5, 'ether')
    assert res.json["milestones"][3]["until"] == 1693094933


def test_projects_patch_w_bad_milestone(client):
    headers = {"authToken": TOKEN_1, "milestones": "badmilestones#-.,"}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code == 400

    assert res.json["status"] == "invalid json"
    res = client.get('/api/projects/1')
    assert res._status_code == 200
    assert len(res.json["milestones"]) == 4


def test_projects_patch_w_bad_id(client):
    headers = {"authToken": TOKEN_1, "webpage": "http://www.example.com"}
    res = client.patch('/api/projects/' + "1" * 400, headers=headers)
    assert res._status_code == 404
    assert res.json["error"] == "Project doesnt exist"
