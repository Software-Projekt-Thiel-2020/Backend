"""Tests for resource donations."""


def test_donations_get(client):
    """get without parameters."""
    res = client.get('/api/donations')
    assert res._status_code == 200
    assert len(res.json) == 4

    assert res.json[0]["id"] == 1
    assert res.json[0]["amount"] == 100
    assert res.json[0]["userid"] == 1
    assert res.json[0]["milestoneid"] == 1

    assert res.json[1]["id"] == 2
    assert res.json[1]["amount"] == 100
    assert res.json[1]["userid"] == 2
    assert res.json[1]["milestoneid"] == 2

    assert res.json[2]["id"] == 3
    assert res.json[2]["amount"] == 100
    assert res.json[2]["userid"] == 3
    assert res.json[2]["milestoneid"] == 3

    assert res.json[3]["id"] == 4
    assert res.json[3]["amount"] == 100
    assert res.json[3]["userid"] == 4
    assert res.json[3]["milestoneid"] == 4
