"""Tests for resource projects."""


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
        '/api/projects?idinstitution=4149515568880992958512407863691161151012446232242436899995657329690652811412908146399707048947103794288197886611300789182395151075411775307886874834113963687061181803401509523685375')
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


"""Following tests will fail: function is not implementet yet"""


def test_projects_id_get_existant_param(client):
    """get for project id with existant id."""
    res = client.get('/api/projects/1')
    assert res._status_code == 200
    assert len(res.json) == 1


def test_projects_id_get_nonexistant_param(client):
    """get for project id with invalid id"""
    res = client.get('/api/projects/1337')
    assert res._status_code == 200
    assert len(res.json) == 0


def test_projects_id_get_bad_value(client):
    """get for project id with bad value"""
    res = client.get('/api/projects/asjdngkjrengskj')
    assert res._status_code == 400
    assert len(res.json) == 1


def test_projects_id_get_big_value(client):
    """get for project id with very big int as id"""
    res = client.get('/api/projects/111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')
    assert res._status_code == 200
    assert len(res.json) == 0
