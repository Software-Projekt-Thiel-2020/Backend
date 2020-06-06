"""Tests for BlockstackAuth."""

from backend.blockstack_auth import BlockstackAuth

# sw2020testuser1.id.blockstack
TOKEN_1 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NksifQ.eyJqdGkiOiIyNGE1OTFkNS1lOGJiLTQwMzYtYWE0Ni1hNzg5MjU2ZDVjZDYiLCJp" \
          "YXQiOjE1OTEyMjUyMzIsImV4cCI6MTU5MzgxNzIzMiwiaXNzIjoiZGlkOmJ0Yy1hZGRyOjE0Z1N4eFhZdzlXbTNoYWoxaGVKYXQ1ZGd" \
          "peHF0YVJ3a3MiLCJwcml2YXRlX2tleSI6IjdiMjI2OTc2MjIzYTIyNjEzMDMwMzA2NjY0MzAzNDY2NjIzNzM0MzQzNzM5MzM2NTM2Mz" \
          "A2MTY1NjYzMDM4MzE2NDYzNjMzMzY1MzEzNDIyMmMyMjY1NzA2ODY1NmQ2NTcyNjE2YzUwNGIyMjNhMjIzMDMyNjYzNDYxMzMzMTYyM" \
          "zA2NDY1NjY2MjM4MzkzNTM4MzY2NjY1NjIzMzM5MzY2MTYzMzE2MzYzNjYzMzYzMzg2NjY1NjM2MzM4NjM2NjMwNjMzNTM2MzMzODYx" \
          "MzEzMDYzMzAzNDM4NjYzOTM1MzEzMzMwMzY2NTY1MzEzNzY1MzgyMjJjMjI2MzY5NzA2ODY1NzI1NDY1Nzg3NDIyM2EyMjM1MzAzOTM" \
          "4MzMzOTM5MzQ2MzY2NjMzODMyMzQ2MjY2Mzc2MjYyMzczNzMwMzM2MzM3NjM2NTMzMzU2NDYzNjI2NDYyMzUzMzM0NjU2NTYzNjQ2Mz" \
          "MyNjIzODMwNjEzNzYzNjQzOTM0MzU2NDYzNjMzOTM1MzkzOTM0MzQzNDY1MzY2MzM4MzY2MzMyMzU2NjM4NjM2MjM1NjEzMjMxMzkzM" \
          "zMzNjEzOTM5MzMzODYxMzY2MzMxNjI2NDMwMzg2NTM1MzkzMTM2NjI2MjMxNjY2NTM2MzIzNjYzNjYzNDY2NjM2NDMyMzEzMjMzNjM2" \
          "MTM1MzkzNTYyMzkzNjMxMzAzNzMyMzgzMTYzMzkzNTYxMzc2MTY1MzAzMzY2NjIzNjMwNjM2MjY2MzE2MjMyMzIzNTY0MzUzMTMzMzA" \
          "zNzMwMjIyYzIyNmQ2MTYzMjIzYTIyNjM2MzY2MzQ2NTYxNjQ2NTM4MzMzMTM0MzA2MzMxMzAzNjM0MzEzMDMyNjI2NTMyMzA2MzY1Mz" \
          "M2NDY0MzEzMDYyMzM2NDM3NjIzMjMxMzg2MjM4NjQzODM3MzgzNzYzMzk2NTY0Mzc2NDYxNjIzMDYzMzQzNTM5MzAzMDM3MzkyMjJjM" \
          "jI3NzYxNzM1Mzc0NzI2OTZlNjcyMjNhNzQ3Mjc1NjU3ZCIsInB1YmxpY19rZXlzIjpbIjAzOWJlYzg2OTEwZWJmZWYwZThmYTdiYTY5" \
          "NDUxZTVmOWM0NTU2OGZkMWEyZjgwNDkzMzYxYWUzNTM4YzY3ZjdiYiJdLCJwcm9maWxlIjpudWxsLCJ1c2VybmFtZSI6InN3MjAyMHR" \
          "lc3R1c2VyMS5pZC5ibG9ja3N0YWNrIiwiY29yZV90b2tlbiI6bnVsbCwiZW1haWwiOm51bGwsInByb2ZpbGVfdXJsIjoiaHR0cHM6Ly" \
          "9nYWlhLmJsb2Nrc3RhY2sub3JnL2h1Yi8xNGdTeHhYWXc5V20zaGFqMWhlSmF0NWRnaXhxdGFSd2tzL3Byb2ZpbGUuanNvbiIsImh1Y" \
          "lVybCI6Imh0dHBzOi8vaHViLmJsb2Nrc3RhY2sub3JnIiwiYmxvY2tzdGFja0FQSVVybCI6Imh0dHBzOi8vY29yZS5ibG9ja3N0YWNr" \
          "Lm9yZyIsImFzc29jaWF0aW9uVG9rZW4iOiJleUowZVhBaU9pSktWMVFpTENKaGJHY2lPaUpGVXpJMU5rc2lmUS5leUpqYUdsc1pGUnZ" \
          "RWE56YjJOcFlYUmxJam9pTURJME1tRXpOR0ZpTTJFeFpUUmtabU5pTXpjd056QTFZelUyTVdNelpEVXdPV0prTURneU16Vm1NVGRpWm" \
          "pReFpEZzFPRFJrWkRNM01EZGpaVEkyWkdVeUlpd2lhWE56SWpvaU1ETTVZbVZqT0RZNU1UQmxZbVpsWmpCbE9HWmhOMkpoTmprME5UR" \
          "mxOV1k1WXpRMU5UWTRabVF4WVRKbU9EQTBPVE16TmpGaFpUTTFNemhqTmpkbU4ySmlJaXdpWlhod0lqb3hOakl5TnpZeE1qTXlMakF5" \
          "TENKcFlYUWlPakUxT1RFeU1qVXlNekl1TURJc0luTmhiSFFpT2lKaFl6RTFaR1EwWWpKbE5HRTJOVFkwT0Roa05qUXhZVFExTm1NMll" \
          "qVTVOeUo5LkRXbl9kNVBmQ0NxVmRnMUV2Rl9velNULXlCRFcwcGFVWXFwZGYxbjZ1WGpZY0xOUmUzQW1FSGtDSTZLWS0xTVNQWG05SU" \
          "ljZmlZb1Mtd0JpWXV4d05nIiwidmVyc2lvbiI6IjEuMy4xIn0.PljXRkEKvUHIZJwll4CVBgGfVrfSaxltRo47dHEiJHmCVuYwGiTii" \
          "hZShJLjS5URoh_TUpdLMlH1ookLjF4Ehw"

# sw2020testuser2.id.blockstack
TOKEN_2 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NksifQ.eyJqdGkiOiIxZjJiYzcyNy03Y2ZhLTQ5NDEtOTk4ZC03YjIyMGEwOTg2NmYiLCJp" \
          "YXQiOjE1OTEyMjU0OTYsImV4cCI6MTU5MzgxNzQ5NiwiaXNzIjoiZGlkOmJ0Yy1hZGRyOjFIMlQxY0Rmd3lZZFlra1pFUkhmQUh4SkJ" \
          "xaDNieTlWd2kiLCJwcml2YXRlX2tleSI6IjdiMjI2OTc2MjIzYTIyMzAzMTMxMzIzNTY0MzMzMzM1MzMzNDYxNjYzMDM0MzE2NTM1Mz" \
          "czNDMyMzczMjMwNjU2MzM0Mzk2MzMwMzY2NjIyMmMyMjY1NzA2ODY1NmQ2NTcyNjE2YzUwNGIyMjNhMjIzMDMzMzQ2MzM4MzgzNzM4M" \
          "zczNTM1MzAzMjM2MzI2MTM3MzI2NjMyNjE2MzY0MzUzMTMxNjY2NjM5MzczNTM3NjMzMTYzNjU2NDM3NjUzNjY2NjU2MjMzNjYzOTMy" \
          "MzQzNTY0MzQ2NjMxNjIzMjYxMzE2MTM0Mzk2MzM0MzMzNjMxMzAyMjJjMjI2MzY5NzA2ODY1NzI1NDY1Nzg3NDIyM2EyMjM5NjYzNzY" \
          "0MzMzNTM0NjQ2NTM3MzAzNjYzMzM2NjY0MzMzODM0MzAzNTY2MzUzOTY1NjMzODM5MzAzMTM3MzIzMjMwMzE2NDY2MzEzMTYzMzc2NT" \
          "M4MzczMzM4NjUzNzY1MzA2NjMyNjUzNzY1MzM2MjM1NjQzOTMzNjE2MTMxNjQ2MzYyMzgzNDYzMzA2NTM2NjY2NDYyNjY2MTM2NjIzM" \
          "DMyNjEzNTMzMzYzMTY2NjYzODYzNjUzMjYxNjQ2MTYyNjYzMjM5MzM2NTMzMzEzOTM0MzQzOTM5NjM2NDYzNjQzNDMxNjQzMjY2Mzkz" \
          "MjM4MzA2MzY1MzEzNDY2NjEzOTYzNjE2MzY0NjYzNzM1NjUzNzMwNjM2NjYzNjY2MzYxNjQzNDY1MzgzMjM4NjQzNjMwMzAzNzM0NjQ" \
          "2MTM4MjIyYzIyNmQ2MTYzMjIzYTIyMzczMDMwNjMzMjY1MzgzMjMzMzE2MzM2NjIzNTYzMzM2MjYxNjIzMTYzMzczNTM2MzUzNjM1Nj" \
          "E2NDYzMzU2MjYxNjYzMzMxMzczODY0MzY2MTYxMzEzNTM4MzUzNjY2MzkzNDM3MzA2MzYzNjM2MzY2NjYzOTMwMzUzNjM2NjMyMjJjM" \
          "jI3NzYxNzM1Mzc0NzI2OTZlNjcyMjNhNzQ3Mjc1NjU3ZCIsInB1YmxpY19rZXlzIjpbIjAzODM0YTYxMjc1NzQ3OGIyOWEwZTRmMDE1" \
          "N2IyNzBhOTc5NTM3NzUxNWE2MmQwYTYzYTI1ZDU2MGYwODE4ZTk1YiJdLCJwcm9maWxlIjpudWxsLCJ1c2VybmFtZSI6InN3MjAyMHR" \
          "lc3R1c2VyMi5pZC5ibG9ja3N0YWNrIiwiY29yZV90b2tlbiI6bnVsbCwiZW1haWwiOm51bGwsInByb2ZpbGVfdXJsIjoiaHR0cHM6Ly" \
          "9nYWlhLmJsb2Nrc3RhY2sub3JnL2h1Yi8xSDJUMWNEZnd5WWRZa2taRVJIZkFIeEpCcWgzYnk5VndpL3Byb2ZpbGUuanNvbiIsImh1Y" \
          "lVybCI6Imh0dHBzOi8vaHViLmJsb2Nrc3RhY2sub3JnIiwiYmxvY2tzdGFja0FQSVVybCI6Imh0dHBzOi8vY29yZS5ibG9ja3N0YWNr" \
          "Lm9yZyIsImFzc29jaWF0aW9uVG9rZW4iOiJleUowZVhBaU9pSktWMVFpTENKaGJHY2lPaUpGVXpJMU5rc2lmUS5leUpqYUdsc1pGUnZ" \
          "RWE56YjJOcFlYUmxJam9pTURNd1lUY3dPV1E1WVRFMk1tUXdaV0kxTmpsbFltRTFZbVExTUdNeE0yWTJOak00T0RFNE9UbG1OV1ZrT1" \
          "RBMVlXUmxNamcwWm1JNVpXUTFOemRpTnpZM0lpd2lhWE56SWpvaU1ETTRNelJoTmpFeU56VTNORGM0WWpJNVlUQmxOR1l3TVRVM1lqS" \
          "TNNR0U1TnprMU16YzNOVEUxWVRZeVpEQmhOak5oTWpWa05UWXdaakE0TVRobE9UVmlJaXdpWlhod0lqb3hOakl5TnpZeE5EazJMak0z" \
          "TVN3aWFXRjBJam94TlRreE1qSTFORGsyTGpNM01Td2ljMkZzZENJNklqY3paR0ZqTVdZMU9UVXhZbU0wWmpNeVl6UTBNamN5TXpKall" \
          "UUmhORGN4SW4wLkxvZlFacFlSaktxd0tuOXQ2VFNEdGVlUUxWSlYyZzA1Nm9NVXBVSEtQUXUxSGg4TGlUU29JaUNBV05qbV9idTJhYm" \
          "NVLThla2dpUU5NUy15VUVVRUVBIiwidmVyc2lvbiI6IjEuMy4xIn0.BhUkt3dAOPkO9xiHAflynVuAtmyoSVGb4TUxFlNhL-6Mc4sVw" \
          "N1yiP2_cyxJlzKBeYumqtNLnWTmlOV8XhrtXQ"


def test_username1():
    assert BlockstackAuth.get_username_from_token(TOKEN_1) == "sw2020testuser1.id.blockstack"


def test_username2():
    assert BlockstackAuth.get_username_from_token(TOKEN_2) == "sw2020testuser2.id.blockstack"


def test_shorten1():
    assert len(BlockstackAuth.short_jwt(TOKEN_1)) < len(TOKEN_1)


def test_shorten2():
    assert len(BlockstackAuth.short_jwt(TOKEN_2)) < len(TOKEN_2)


def test_verify_valid1():
    assert BlockstackAuth.verify_auth_response(TOKEN_1)


def test_verify_valid2():
    assert BlockstackAuth.verify_auth_response(TOKEN_2)
