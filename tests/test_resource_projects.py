"""Tests for resource projects."""
import json

from .test_blockstackauth import TOKEN_1


def test_projects_get(client):
    """get without parameters."""
    res = client.get('/api/projects')
    assert res._status_code == 200
    assert len(res.json) == 3

    assert res.json[0]["id"] == 1
    assert res.json[0]["idinstitution"] == 1
    assert res.json[0]["idsmartcontract"] == 2
    assert res.json[0]["name"] == "Computer malt Bild"
    assert res.json[0]["webpage"] == "www.cmb.de"

    assert res.json[1]["id"] == 2
    assert res.json[1]["idinstitution"] == 3
    assert res.json[1]["idsmartcontract"] == 2
    assert res.json[1]["name"] == "Rangaroek verteidigen"
    assert res.json[1]["webpage"] == "www.asgard.as"

    assert res.json[2]["id"] == 3
    assert res.json[2]["idinstitution"] == 3
    assert res.json[2]["idsmartcontract"] == 2
    assert res.json[2]["name"] == "Softwareprojekt 2020"
    assert res.json[2]["webpage"] == "www.swp.de"


def test_projects_get_w_institution(client):
    """get with id_institution."""
    res = client.get('/api/projects?idinstitution=3')
    assert res._status_code == 200
    assert len(res.json) == 2

    assert res.json[0]["id"] == 2
    assert res.json[0]["idinstitution"] == 3
    assert res.json[0]["idsmartcontract"] == 2
    assert res.json[0]["name"] == "Rangaroek verteidigen"
    assert res.json[0]["webpage"] == "www.asgard.as"

    assert res.json[1]["id"] == 3
    assert res.json[1]["idinstitution"] == 3
    assert res.json[1]["idsmartcontract"] == 2
    assert res.json[1]["name"] == "Softwareprojekt 2020"
    assert res.json[1]["webpage"] == "www.swp.de"


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
    assert len(res.json) == 6

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["idsmartcontract"] == 2
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["webpage"] == "www.cmb.de"

    assert len(res.json["milestones"]) == 4
    assert res.json["milestones"][0]["id"] == 1
    assert res.json["milestones"][0]["idProjekt"] == 1
    assert res.json["milestones"][0]["goal"] == 1000
    assert res.json["milestones"][0]["requiredVotes"] == 112
    assert res.json["milestones"][0]["currentVotes"] == 112
    assert res.json["milestones"][0]["until"] == 600000

    assert res.json["milestones"][1]["id"] == 2
    assert res.json["milestones"][1]["idProjekt"] == 1
    assert res.json["milestones"][1]["goal"] == 2000
    assert res.json["milestones"][1]["requiredVotes"] == 112
    assert res.json["milestones"][1]["currentVotes"] == 12
    assert res.json["milestones"][1]["until"] == 1200000

    assert res.json["milestones"][2]["id"] == 3
    assert res.json["milestones"][2]["idProjekt"] == 1
    assert res.json["milestones"][2]["goal"] == 3000
    assert res.json["milestones"][2]["requiredVotes"] == 112
    assert res.json["milestones"][2]["currentVotes"] == 0
    assert res.json["milestones"][2]["until"] == 2400000

    assert res.json["milestones"][3]["id"] == 7
    assert res.json["milestones"][3]["idProjekt"] == 1
    assert res.json["milestones"][3]["goal"] == 5000
    assert res.json["milestones"][3]["requiredVotes"] == 666
    assert res.json["milestones"][3]["currentVotes"] == 400
    assert res.json["milestones"][3]["until"] == 100000000


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


def test_projects_post_required_params(client):
    headers = {"authToken": TOKEN_1, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1592094933}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 201
    assert res.json["status"] == "ok"

    res = client.get('/api/projects/4')
    assert res._status_code == 200
    assert len(res.json) == 6

    assert res.json["id"] == 4
    assert res.json["idinstitution"] is None
    assert res.json["idsmartcontract"] == 1
    assert res.json["name"] == headers["name"]
    assert res.json["webpage"] is None
    assert len(res.json["milestones"]) == 0


def test_projects_post_w_bad_milestones(client):
    headers = {"authToken": TOKEN_1, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1592094933,
               "milestones": "dennis"}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 400
    assert res.json["status"] == "invalid json"


def test_projects_post_w_milestones(client):
    milestones = [
        {"goal": 1000, "requiredVotes": 1337, "until": 1592094933},
        {"goal": 5000, "requiredVotes": 42, "until": 1592094932},
    ]
    headers = {"authToken": TOKEN_1, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1592094933,
               "milestones": json.dumps(milestones)}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 201
    assert res.json["status"] == "ok"

    res = client.get('/api/projects/4')
    assert res._status_code == 200
    assert len(res.json) == 6

    assert res.json["id"] == 4
    assert res.json["idinstitution"] is None
    assert res.json["idsmartcontract"] == 1
    assert res.json["name"] == headers["name"]
    assert res.json["webpage"] is None

    assert len(res.json["milestones"]) == 2
    assert res.json["milestones"][0]["id"] == 8
    assert res.json["milestones"][0]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][0]["goal"] == milestones[0]["goal"]
    assert res.json["milestones"][0]["requiredVotes"] == milestones[0]["requiredVotes"]
    assert res.json["milestones"][0]["currentVotes"] == 0
    assert res.json["milestones"][0]["until"] == milestones[0]["until"]

    assert res.json["milestones"][1]["id"] == 9
    assert res.json["milestones"][1]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][1]["goal"] == milestones[1]["goal"]
    assert res.json["milestones"][1]["requiredVotes"] == milestones[1]["requiredVotes"]
    assert res.json["milestones"][1]["currentVotes"] == 0
    assert res.json["milestones"][1]["until"] == milestones[1]["until"]


def test_projects_post_w_webpage(client):
    headers = {"authToken": TOKEN_1, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1592094933,
               "webpage": "http://www.example.com"}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 201
    assert res.json["status"] == "ok"

    res = client.get('/api/projects/4')
    assert res._status_code == 200
    assert len(res.json) == 6

    assert res.json["id"] == 4
    assert res.json["idinstitution"] is None
    assert res.json["idsmartcontract"] == 1
    assert res.json["name"] == headers["name"]
    assert res.json["webpage"] == headers["webpage"]
    assert len(res.json["milestones"]) == 0


def test_projects_post_w_bad_webpage(client):
    headers = {"authToken": TOKEN_1, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1592094933,
               "webpage": "notaurl#22*3\\asdf"}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 400
    assert res.json["error"] == "webpage is not a valid url"


def test_projects_post_w_institution(client):
    headers = {"authToken": TOKEN_1, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1592094933,
               "idInstitution": 3}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 201
    assert res.json["status"] == "ok"

    res = client.get('/api/projects/4')
    assert res._status_code == 200
    assert len(res.json) == 6

    assert res.json["id"] == 4
    assert res.json["idinstitution"] == headers["idInstitution"]
    assert res.json["idsmartcontract"] == 1
    assert res.json["name"] == headers["name"]
    assert res.json["webpage"] is None
    assert len(res.json["milestones"]) == 0


def test_projects_post_w_bad_institution(client):
    headers = {"authToken": TOKEN_1, "name": "example", "goal": 5000, "requiredVotes": "1337", "until": 1592094933,
               "idInstitution": 30000}
    res = client.post('/api/projects', headers=headers)
    assert res._status_code == 400


def test_projects_patch_w_webpage(client):
    headers = {"authToken": TOKEN_1, "webpage": "http://www.example.com"}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code == 201
    assert res.json["status"] == "ok"

    res = client.get('/api/projects/1')
    assert res._status_code == 200
    assert len(res.json) == 6

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["idsmartcontract"] == 2
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["webpage"] == headers["webpage"]

    assert len(res.json["milestones"]) == 4


def test_projects_patch_w_bad_webpage(client):
    headers = {"authToken": TOKEN_1, "webpage": "notvalidurl"}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code == 400
    assert res.json["error"] == "webpage is not a valid url"

    res = client.get('/api/projects/1')
    assert res._status_code == 200
    assert len(res.json) == 6

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["idsmartcontract"] == 2
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["webpage"] == "www.cmb.de"

    assert len(res.json["milestones"]) == 4


def test_projects_patch_wo_auth_wo_params(client):
    res = client.patch('/api/projects/1')
    assert res._status_code == 401


def test_projects_patch_w_milestones(client):
    milestones = [
        {"goal": 1000, "requiredVotes": 1337, "until": 1592094933},
        {"goal": 5000, "requiredVotes": 42, "until": 1592094932},
    ]
    headers = {"authToken": TOKEN_1, "milestones": json.dumps(milestones)}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code == 201

    assert res.json["status"] == "ok"
    res = client.get('/api/projects/1')
    assert res._status_code == 200
    assert len(res.json) == 6

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["idsmartcontract"] == 2
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["webpage"] == "www.cmb.de"

    assert len(res.json["milestones"]) == 6
    assert res.json["milestones"][0]["id"] == 1
    assert res.json["milestones"][0]["idProjekt"] == 1
    assert res.json["milestones"][0]["goal"] == 1000
    assert res.json["milestones"][0]["requiredVotes"] == 112
    assert res.json["milestones"][0]["currentVotes"] == 112
    assert res.json["milestones"][0]["until"] == 600000

    assert res.json["milestones"][1]["id"] == 2
    assert res.json["milestones"][1]["idProjekt"] == 1
    assert res.json["milestones"][1]["goal"] == 2000
    assert res.json["milestones"][1]["requiredVotes"] == 112
    assert res.json["milestones"][1]["currentVotes"] == 12
    assert res.json["milestones"][1]["until"] == 1200000

    assert res.json["milestones"][2]["id"] == 3
    assert res.json["milestones"][2]["idProjekt"] == 1
    assert res.json["milestones"][2]["goal"] == 3000
    assert res.json["milestones"][2]["requiredVotes"] == 112
    assert res.json["milestones"][2]["currentVotes"] == 0
    assert res.json["milestones"][2]["until"] == 2400000

    assert res.json["milestones"][3]["id"] == 7
    assert res.json["milestones"][3]["idProjekt"] == 1
    assert res.json["milestones"][3]["goal"] == 5000
    assert res.json["milestones"][3]["requiredVotes"] == 666
    assert res.json["milestones"][3]["currentVotes"] == 400
    assert res.json["milestones"][3]["until"] == 100000000

    assert res.json["milestones"][4]["id"] == 8
    assert res.json["milestones"][4]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][4]["goal"] == milestones[0]["goal"]
    assert res.json["milestones"][4]["requiredVotes"] == milestones[0]["requiredVotes"]
    assert res.json["milestones"][4]["currentVotes"] == 0
    assert res.json["milestones"][4]["until"] == milestones[0]["until"]

    assert res.json["milestones"][5]["id"] == 9
    assert res.json["milestones"][5]["idProjekt"] == res.json["id"]
    assert res.json["milestones"][5]["goal"] == milestones[1]["goal"]
    assert res.json["milestones"][5]["requiredVotes"] == milestones[1]["requiredVotes"]
    assert res.json["milestones"][5]["currentVotes"] == 0
    assert res.json["milestones"][5]["until"] == milestones[1]["until"]


def test_projects_patch_wo_params(client):
    headers = {"authToken": TOKEN_1}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code == 201

    assert res.json["status"] == "ok"
    res = client.get('/api/projects/1')
    assert res._status_code == 200
    assert len(res.json) == 6

    assert res.json["id"] == 1
    assert res.json["idinstitution"] == 1
    assert res.json["idsmartcontract"] == 2
    assert res.json["name"] == "Computer malt Bild"
    assert res.json["webpage"] == "www.cmb.de"

    assert len(res.json["milestones"]) == 4
    assert res.json["milestones"][0]["id"] == 1
    assert res.json["milestones"][0]["idProjekt"] == 1
    assert res.json["milestones"][0]["goal"] == 1000
    assert res.json["milestones"][0]["requiredVotes"] == 112
    assert res.json["milestones"][0]["currentVotes"] == 112
    assert res.json["milestones"][0]["until"] == 600000

    assert res.json["milestones"][1]["id"] == 2
    assert res.json["milestones"][1]["idProjekt"] == 1
    assert res.json["milestones"][1]["goal"] == 2000
    assert res.json["milestones"][1]["requiredVotes"] == 112
    assert res.json["milestones"][1]["currentVotes"] == 12
    assert res.json["milestones"][1]["until"] == 1200000

    assert res.json["milestones"][2]["id"] == 3
    assert res.json["milestones"][2]["idProjekt"] == 1
    assert res.json["milestones"][2]["goal"] == 3000
    assert res.json["milestones"][2]["requiredVotes"] == 112
    assert res.json["milestones"][2]["currentVotes"] == 0
    assert res.json["milestones"][2]["until"] == 2400000

    assert res.json["milestones"][3]["id"] == 7
    assert res.json["milestones"][3]["idProjekt"] == 1
    assert res.json["milestones"][3]["goal"] == 5000
    assert res.json["milestones"][3]["requiredVotes"] == 666
    assert res.json["milestones"][3]["currentVotes"] == 400
    assert res.json["milestones"][3]["until"] == 100000000


def test_projects_patch_w_bad_milestone(client):
    headers = {"authToken": TOKEN_1, "milestones": "badmilestones#-.,"}
    res = client.patch('/api/projects/1', headers=headers)
    assert res._status_code == 400

    assert res.json["status"] == "invalid json"
    res = client.get('/api/projects/1')
    assert res._status_code == 200
    assert len(res.json) == 6
    assert len(res.json["milestones"]) == 4


def test_projects_patch_w_bad_id(client):
    headers = {"authToken": TOKEN_1, "webpage": "http://www.example.com"}
    res = client.patch('/api/projects/' + "1" * 400, headers=headers)
    assert res._status_code == 404
    assert res.json["error"] == "Project doesnt exist"
