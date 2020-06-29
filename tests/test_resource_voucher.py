"""Tests for resource voucher."""
from datetime import datetime, timedelta

from tests.test_blockstackauth import TOKEN_1, TOKEN_2


def test_voucher_institution_get(client):
    res = client.get('/api/vouchers/institution')
    assert res._status_code == 200
    assert len(res.json) == 2

    assert res.json[0]["id"] == 1
    assert res.json[0]["amount"] == 2
    assert res.json[0]["institutionid"] == 1
    assert res.json[0]["institutionName"] == "MSGraphic"
    assert res.json[0]["subject"] == "Der Computer malt ein täuschend echtes Bild für sie"
    assert res.json[0]["title"] == "Von Computer gemaltes Bild"
    assert res.json[0]["validTime"] == 2 * 31536000
    assert not res.json[0]["available"]
    assert res.json[0]["price"] == 1000

    assert res.json[1]["id"] == 2
    assert res.json[1]["amount"] == 2
    assert res.json[1]["institutionid"] == 1
    assert res.json[1]["institutionName"] == "MSGraphic"
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
    assert res.json[1]["institutionName"] == "MSGraphic"
    assert res.json[0]["subject"] == "Der Computer malt ein täuschend echtes Bild für sie"
    assert res.json[0]["title"] == "Von Computer gemaltes Bild"
    assert res.json[0]["validTime"] == 2 * 31536000
    assert not res.json[0]["available"]
    assert res.json[0]["price"] == 1000

    assert res.json[1]["id"] == 2
    assert res.json[1]["amount"] == 2
    assert res.json[1]["institutionid"] == 1
    assert res.json[1]["institutionName"] == "MSGraphic"
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


def test_voucher_user_get(client):
    res = client.get('/api/vouchers/user')
    assert res._status_code == 200
    assert len(res.json) == 4

    assert res.json[0]["id"] == 1
    assert res.json[0]["userid"] == 1
    assert res.json[0]["idvoucher"] == 1
    assert res.json[0]["untilTime"] == datetime(2020, 1, 1).timestamp()
    assert not res.json[0]["used"]
    assert res.json[0]["price"] == 1000

    assert res.json[1]["id"] == 2
    assert res.json[1]["userid"] == 2
    assert res.json[1]["idvoucher"] == 2
    assert res.json[1]["untilTime"] == datetime(2022, 5, 17).timestamp()
    assert not res.json[1]["used"]
    assert res.json[1]["price"] == 2000

    assert res.json[2]["id"] == 3
    assert res.json[2]["userid"] == 6
    assert res.json[2]["idvoucher"] == 1
    assert res.json[2]["untilTime"] == datetime(2022, 1, 13).timestamp()
    assert not res.json[2]["used"]
    assert res.json[2]["price"] == 1000

    assert res.json[3]["id"] == 4
    assert res.json[3]["userid"] == 7
    assert res.json[3]["idvoucher"] == 2
    assert res.json[3]["untilTime"] == datetime(2021, 5, 17).timestamp()
    assert res.json[3]["used"]
    assert res.json[3]["price"] == 2000


def test_voucher_user_get_id(client):
    res = client.get('/api/vouchers/user?id=3')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 3
    assert res.json[0]["userid"] == 6
    assert res.json[0]["idvoucher"] == 1
    assert res.json[0]["untilTime"] == datetime(2022, 1, 13).timestamp()
    assert not res.json[0]["used"]
    assert res.json[0]["price"] == 1000


def test_voucher_user_get_idvoucher(client):
    res = client.get('/api/vouchers/user?idVoucher=2')
    assert res._status_code == 200
    assert len(res.json) == 2

    assert res.json[0]["id"] == 2
    assert res.json[0]["userid"] == 2
    assert res.json[0]["idvoucher"] == 2
    assert res.json[0]["untilTime"] == datetime(2022, 5, 17).timestamp()
    assert not res.json[0]["used"]
    assert res.json[0]["price"] == 2000

    assert res.json[1]["id"] == 4
    assert res.json[1]["userid"] == 7
    assert res.json[1]["idvoucher"] == 2
    assert res.json[1]["untilTime"] == datetime(2021, 5, 17).timestamp()
    assert res.json[1]["used"]
    assert res.json[1]["price"] == 2000


def test_voucher_user_get_iduser(client):
    res = client.get('/api/vouchers/user?idUser=1')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["userid"] == 1
    assert res.json[0]["idvoucher"] == 1
    assert res.json[0]["untilTime"] == datetime(2020, 1, 1).timestamp()
    assert not res.json[0]["used"]
    assert res.json[0]["price"] == 1000


def test_voucher_user_get_used(client):
    res = client.get('/api/vouchers/user?used=1')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 4
    assert res.json[0]["userid"] == 7
    assert res.json[0]["idvoucher"] == 2
    assert res.json[0]["untilTime"] == datetime(2021, 5, 17).timestamp()
    assert res.json[0]["used"]
    assert res.json[0]["price"] == 2000


def test_voucher_user_get_used2(client):
    res = client.get('/api/vouchers/user?used=0')
    assert res._status_code == 200
    assert len(res.json) == 3

    assert res.json[0]["id"] == 1
    assert res.json[0]["userid"] == 1
    assert res.json[0]["idvoucher"] == 1
    assert res.json[0]["untilTime"] == datetime(2020, 1, 1).timestamp()
    assert not res.json[0]["used"]
    assert res.json[0]["price"] == 1000

    assert res.json[1]["id"] == 2
    assert res.json[1]["userid"] == 2
    assert res.json[1]["idvoucher"] == 2
    assert res.json[1]["untilTime"] == datetime(2022, 5, 17).timestamp()
    assert not res.json[1]["used"]
    assert res.json[1]["price"] == 2000

    assert res.json[2]["id"] == 3
    assert res.json[2]["userid"] == 6
    assert res.json[2]["idvoucher"] == 1
    assert res.json[2]["untilTime"] == datetime(2022, 1, 13).timestamp()
    assert not res.json[2]["used"]
    assert res.json[2]["price"] == 1000


def test_voucher_user_expired(client):
    res = client.get('/api/vouchers/user?expired=1')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 1
    assert res.json[0]["userid"] == 1
    assert res.json[0]["idvoucher"] == 1
    assert res.json[0]["untilTime"] == datetime(2020, 1, 1).timestamp()
    assert not res.json[0]["used"]
    assert res.json[0]["price"] == 1000


def test_voucher_user_expired2(client):
    res = client.get('/api/vouchers/user?expired=0')
    assert res._status_code == 200
    assert len(res.json) == 3

    assert res.json[0]["id"] == 2
    assert res.json[0]["userid"] == 2
    assert res.json[0]["idvoucher"] == 2
    assert res.json[0]["untilTime"] == datetime(2022, 5, 17).timestamp()
    assert not res.json[0]["used"]
    assert res.json[0]["price"] == 2000

    assert res.json[1]["id"] == 3
    assert res.json[1]["userid"] == 6
    assert res.json[1]["idvoucher"] == 1
    assert res.json[1]["untilTime"] == datetime(2022, 1, 13).timestamp()
    assert not res.json[1]["used"]
    assert res.json[1]["price"] == 1000

    assert res.json[2]["id"] == 4
    assert res.json[2]["userid"] == 7
    assert res.json[2]["idvoucher"] == 2
    assert res.json[2]["untilTime"] == datetime(2021, 5, 17).timestamp()
    assert res.json[2]["used"]
    assert res.json[2]["price"] == 2000


def test_voucher_user_delete(client):
    headers = {"authToken": TOKEN_1, "id": 3}
    res = client.delete('/api/vouchers/user', headers=headers)
    assert res._status_code == 201

    res = client.get('/api/vouchers/user?used=0')
    assert res._status_code == 200
    assert len(res.json) == 2

    assert res.json[0]["id"] == 1
    assert res.json[0]["userid"] == 1
    assert res.json[0]["idvoucher"] == 1
    assert res.json[0]["untilTime"] == datetime(2020, 1, 1).timestamp()
    assert not res.json[0]["used"]
    assert res.json[0]["price"] == 1000

    assert res.json[1]["id"] == 2
    assert res.json[1]["userid"] == 2
    assert res.json[1]["idvoucher"] == 2
    assert res.json[1]["untilTime"] == datetime(2022, 5, 17).timestamp()
    assert not res.json[1]["used"]
    assert res.json[1]["price"] == 2000

    res = client.get('/api/vouchers/user?used=1')
    assert res._status_code == 200
    assert len(res.json) == 2

    assert res.json[0]["id"] == 3
    assert res.json[0]["userid"] == 6
    assert res.json[0]["idvoucher"] == 1
    assert res.json[0]["untilTime"] == datetime(2022, 1, 13).timestamp()
    assert res.json[0]["used"]
    assert res.json[0]["price"] == 1000

    assert res.json[1]["id"] == 4
    assert res.json[1]["userid"] == 7
    assert res.json[1]["idvoucher"] == 2
    assert res.json[1]["untilTime"] == datetime(2021, 5, 17).timestamp()
    assert res.json[1]["used"]
    assert res.json[1]["price"] == 2000


def test_voucher_user_delete_bad_id(client):
    headers = {"authToken": TOKEN_1, "id": 2}
    res = client.delete('/api/vouchers/user', headers=headers)
    assert res._status_code == 404

    res = client.get('/api/vouchers/user?used=1')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 4
    assert res.json[0]["userid"] == 7
    assert res.json[0]["idvoucher"] == 2
    assert res.json[0]["untilTime"] == datetime(2021, 5, 17).timestamp()
    assert res.json[0]["used"]
    assert res.json[0]["price"] == 2000


def test_voucher_user_delete_bad_id2(client):
    headers = {"authToken": TOKEN_1, "id": 1337}
    res = client.delete('/api/vouchers/user', headers=headers)
    assert res._status_code == 404

    res = client.get('/api/vouchers/user?used=1')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 4
    assert res.json[0]["userid"] == 7
    assert res.json[0]["idvoucher"] == 2
    assert res.json[0]["untilTime"] == datetime(2021, 5, 17).timestamp()
    assert res.json[0]["used"]
    assert res.json[0]["price"] == 2000


def test_voucher_user_delete_bad_user(client):
    headers = {"authToken": TOKEN_2, "id": 2}
    res = client.delete('/api/vouchers/user', headers=headers)
    assert res._status_code == 404

    res = client.get('/api/vouchers/user?used=1')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 4
    assert res.json[0]["userid"] == 7
    assert res.json[0]["idvoucher"] == 2
    assert res.json[0]["untilTime"] == datetime(2021, 5, 17).timestamp()
    assert res.json[0]["used"]
    assert res.json[0]["price"] == 2000


def test_voucher_user_post(client_w_eth):
    headers = {"authToken": TOKEN_1, "idVoucher": 2}
    # ToDo: Add balance
    res = client_w_eth.post('/api/vouchers/user', headers=headers)
    assert res._status_code == 200

    res = client_w_eth.get('/api/vouchers/user?idUser=6')
    assert res._status_code == 200
    assert len(res.json) == 2

    assert res.json[0]["id"] == 3
    assert res.json[0]["userid"] == 6
    assert res.json[0]["idvoucher"] == 1
    assert res.json[0]["untilTime"] == datetime(2022, 1, 13).timestamp()
    assert not res.json[0]["used"]
    assert res.json[0]["price"] == 1000

    assert res.json[1]["id"] == 5
    assert res.json[1]["userid"] == 6
    assert res.json[1]["idvoucher"] == 2
    assert int(res.json[1]["untilTime"]) == int((datetime.now() + timedelta(0, 2 * 31536000)).timestamp())
    assert not res.json[1]["used"]
    assert res.json[1]["price"] == 2000


def test_voucher_user_post2(client_w_eth):
    headers = {"authToken": TOKEN_1, "idVoucher": 1}
    # ToDo: Add balance
    res = client_w_eth.post('/api/vouchers/user', headers=headers)
    assert res._status_code == 406

    res = client_w_eth.get('/api/vouchers/user?idUser=6')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 3
    assert res.json[0]["userid"] == 6
    assert res.json[0]["idvoucher"] == 1
    assert res.json[0]["untilTime"] == datetime(2022, 1, 13).timestamp()
    assert not res.json[0]["used"]
    assert res.json[0]["price"] == 1000


def test_voucher_user_post_bad_voucherid(client_w_eth):
    headers = {"authToken": TOKEN_1, "idVoucher": 1337}
    # ToDo: Add balance
    res = client_w_eth.post('/api/vouchers/user', headers=headers)
    assert res._status_code == 404

    res = client_w_eth.get('/api/vouchers/user?idUser=6')
    assert res._status_code == 200
    assert len(res.json) == 1

    assert res.json[0]["id"] == 3
    assert res.json[0]["userid"] == 6
    assert res.json[0]["idvoucher"] == 1
    assert res.json[0]["untilTime"] == datetime(2022, 1, 13).timestamp()
    assert not res.json[0]["used"]
    assert res.json[0]["price"] == 1000

# ToDo: test_voucher_user_no_funds
