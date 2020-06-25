"""Tests for resource voucher."""


def test_voucher_institution_get(client):
    res = client.get('/api/vouchers/institution')
    assert res._status_code == 200
    assert len(res.json) == 2

    assert res.json[0]["id"] == 1
    assert res.json[0]["amount"] == 2
    assert res.json[0]["institutionid"] == 1
    assert res.json[0]["subject"] == "Der Computer malt ein täuschend echtes Bild für sie"
    assert res.json[0]["title"] == "Von Computer gemaltes Bild"
    assert res.json[0]["validTime"] == 2 * 31536000
    assert not res.json[0]["available"]
    assert res.json[0]["price"] == 1000

    assert res.json[1]["id"] == 2
    assert res.json[1]["amount"] == 2
    assert res.json[1]["institutionid"] == 1
    assert res.json[1]["subject"] == "Software für ein Hochschulprojet"
    assert res.json[1]["title"] == "Software"
    assert res.json[1]["validTime"] == 2 * 31536000
    assert res.json[1]["available"]
    assert res.json[1]["price"] == 2000


def test_voucher_institution_get_idinst(client):
    res = client.get('/api/vouchers/institution?idInstitution=1')
    assert res._status_code == 200
    assert len(res.json) == 2

    assert res.json[0]["id"] == 1
    assert res.json[0]["amount"] == 2
    assert res.json[0]["institutionid"] == 1
    assert res.json[0]["subject"] == "Der Computer malt ein täuschend echtes Bild für sie"
    assert res.json[0]["title"] == "Von Computer gemaltes Bild"
    assert res.json[0]["validTime"] == 2 * 31536000
    assert not res.json[0]["available"]
    assert res.json[0]["price"] == 1000

    assert res.json[1]["id"] == 2
    assert res.json[1]["amount"] == 2
    assert res.json[1]["institutionid"] == 1
    assert res.json[1]["subject"] == "Software für ein Hochschulprojet"
    assert res.json[1]["title"] == "Software"
    assert res.json[1]["validTime"] == 2 * 31536000
    assert res.json[1]["available"]
    assert res.json[1]["price"] == 2000


def test_voucher_institution_get_idinst2(client):
    res = client.get('/api/vouchers/institution?idInstitution=2')
    assert res._status_code == 200
    assert len(res.json) == 0


def test_voucher_institution_get_available(client):
    res = client.get('/api/vouchers/institution?available=1')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 2
    assert res.json[0]["amount"] == 2
    assert res.json[0]["institutionid"] == 1
    assert res.json[0]["subject"] == "Software für ein Hochschulprojet"
    assert res.json[0]["title"] == "Software"
    assert res.json[0]["validTime"] == 2 * 31536000
    assert res.json[0]["available"]
    assert res.json[0]["price"] == 2000


def test_voucher_institution_get_available2(client):
    res = client.get('/api/vouchers/institution?available=0')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["amount"] == 2
    assert res.json[0]["institutionid"] == 1
    assert res.json[0]["subject"] == "Der Computer malt ein täuschend echtes Bild für sie"
    assert res.json[0]["title"] == "Von Computer gemaltes Bild"
    assert res.json[0]["validTime"] == 2 * 31536000
    assert not res.json[0]["available"]
    assert res.json[0]["price"] == 1000


def test_voucher_institution_get_available_bad(client):
    res = client.get('/api/vouchers/institution?available=a')
    assert res._status_code == 400
