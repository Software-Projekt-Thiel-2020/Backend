"""Tests for resource users."""


def test_users_get(client):
    res = client.get('/api/users?username=LoetkolbenLudwig')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["email"] == "ll@swp.de"
    assert res.json[0]["firstname"] == "Ludwig"
    assert res.json[0]["id"] == 1
    assert res.json[0]["lastname"] == "Loetkolben"
    assert res.json[0]["publickey"] == "4242424242"
    assert res.json[0]["username"] == "LoetkolbenLudwig"


def test_users_get_wo_param(client):
    res = client.get('/api/users')
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "missing Argument"


def test_users_get_w_badparam(client):
    res = client.get('/api/users?firstname=Manfred')
    assert res._status_code == 400
    assert len(res.json) == 1
    assert res.json["error"] == "missing Argument"


def test_users_get_w_unknown(client):
    res = client.get('/api/users?username=Dennis')
    assert res._status_code == 200
    assert len(res.json) == 0


def test_users_get_w_numbers(client):
    res = client.get('/api/users?username=123')
    assert res._status_code == 200
    assert len(res.json) == 0


def test_users_get_w_special(client):
    res = client.get('/api/users?username=-,.!#*?')
    assert res._status_code == 200
    assert len(res.json) == 0


def test_users_id_get_existant_param(client):
    """get for users id with existant id."""
    res = client.get('/api/users/1')
    assert res._status_code == 200
    assert len(res.json) == 6


def test_users_id_get_nonexistant_param(client):
    """get for users id with invalid id"""
    res = client.get('/api/users/1337')
    assert res._status_code == 404
    assert len(res.json) == 0


def test_users_id_get_bad_value(client):
    """get for users id with bad value"""
    res = client.get('/api/users/abcdefg')
    assert res._status_code == 400
    assert len(res.json) == 1


def test_users_id_get_big_value(client):
    """get for users id with very big int as id"""
    res = client.get('/api/users/' + "1" * 200)
    assert res._status_code == 404
    assert len(res.json) == 0
