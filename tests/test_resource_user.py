"""Tests for resource users."""

from .test_blockstackauth import TOKEN_1


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


def test_users_get2(client):
    res = client.get('/api/users?username=kolben')
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


def test_users_id_get(client):
    """get for users id with existant id."""
    res = client.get('/api/users/1')
    assert res._status_code == 200
    assert len(res.json) == 6

    assert res.json["id"] == 1
    assert res.json["username"] == "LoetkolbenLudwig"
    assert res.json["firstname"] == "Ludwig"
    assert res.json["lastname"] == "Loetkolben"
    assert res.json["email"] == "ll@swp.de"


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


def test_users_id_get2(client):
    res = client.get('/api/users/6')
    assert res.json["id"] == 6
    assert res.json["username"] == "sw2020testuser1.id.blockstack"
    assert res.json["firstname"] == "testuser1"
    assert res.json["lastname"] == "sw2020"
    assert res.json["email"] == "testuser1@example.com"


def test_users_put(client):
    headers = {"authToken": TOKEN_1, "firstname": "new_firstname", "lastname": "new_lastname", "email": "a@b.com"}
    res = client.put('/api/users', headers=headers)
    assert res._status_code == 200

    res = client.get('/api/users/6')
    assert res._status_code == 200

    assert res.json["id"] == 6
    assert res.json["username"] == "sw2020testuser1.id.blockstack"
    assert res.json["firstname"] == "new_firstname"
    assert res.json["lastname"] == "new_lastname"
    assert res.json["email"] == "a@b.com"


def test_users_put_invalid_email(client):
    headers = {"authToken": TOKEN_1, "firstname": "new_firstname", "lastname": "new_lastname", "email": "dennis"}
    res = client.put('/api/users', headers=headers)
    assert res._status_code == 400
    assert res.json["error"] == "email is not a valid email"

    res = client.get('/api/users/6')
    assert res._status_code == 200

    assert res.json["id"] == 6
    assert res.json["username"] == "sw2020testuser1.id.blockstack"
    assert res.json["firstname"] == "testuser1"
    assert res.json["lastname"] == "sw2020"
    assert res.json["email"] == "testuser1@example.com"


def test_users_put_wo_auth(client):
    headers = {"firstname": "new_firstname", "lastname": "new_lastname", "email": "dennis"}
    res = client.put('/api/users', headers=headers)
    assert res._status_code == 401

    res = client.get('/api/users/6')
    assert res._status_code == 200

    assert res.json["id"] == 6
    assert res.json["username"] == "sw2020testuser1.id.blockstack"
    assert res.json["firstname"] == "testuser1"
    assert res.json["lastname"] == "sw2020"
    assert res.json["email"] == "testuser1@example.com"
