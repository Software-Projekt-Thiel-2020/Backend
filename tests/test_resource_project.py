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
