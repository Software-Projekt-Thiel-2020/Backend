import configparser
import sys
import json
from pathlib import Path

from web3 import Web3


CFG_PARSER: configparser.ConfigParser = configparser.ConfigParser()
CFG_PARSER.read("backend_config.ini")


WEB3: Web3 = Web3(Web3.HTTPProvider(CFG_PARSER["Ethereum"]["URI"]))


if WEB3.isConnected():
    print("connected to ethereum node.")
else:
    print("could not connect to ethereum node.")
    sys.exit(1)


WEB3.eth.defaultAccount = WEB3.eth.accounts[0]

BASE = Path.cwd() / "backend" / "smart_contracts"

with open(str(BASE / "build" / "contracts" / "Project.json")) as json_file:
    PROJECT_JSON: dict = json.load(json_file)

with open(str(BASE / "build" / "contracts" / "Institution.json")) as json_file:
    INSTITUTION_JSON: dict = json.load(json_file)


# Voucher = WEB3.eth.contract(abi=PROJECT_JSON["abi"], bytecode=PROJECT_JSON["bytecode"])
# # owner, partial_percent, name, target_amount, min_donation
# tx_hash = Voucher.constructor(WEB3.eth.accounts[1], 80, WEB3.toBytes(text="test description"), 133337, 10).transact()
# tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash)
#
#
# voucher_inst = WEB3.eth.contract(address=tx_receipt.contractAddress, abi=PROJECT_JSON["abi"])
#
# user_inst = {
#     "publickeyUser": '0x865fefF6a8503405f8a316e53039dc8332a5A60b',
#     "privatekeyUser": b'/8\x9f}\x96\xe9{\xee\x14\x972\x01b\xf3\xb6/\xbcjX\x19J\xfbgW\xd6\x94p\xda\xa6/=\xdf',
# }
#
# print(voucher_inst.functions.greet().call())
# tx_hash2 = voucher_inst.functions.setGreeting("NEW GREETING!").transact()
# tx_receipt2 = WEB3.eth.waitForTransactionReceipt(tx_hash)
# print(voucher_inst.functions.greet().call())
#
# kr = {'nonce': WEB3.eth.getTransactionCount(user_inst["publickeyUser"]),
#       'from': user_inst["publickeyUser"],
#       'gas': 2000000,
#       'gasPrice': WEB3.toWei('50', 'gwei'),  # ToDo: ?
#       }
# tx_hash3 = voucher_inst.functions.register().buildTransaction(kr)
# print("tx: ", tx_hash3)
#
#
#
#
# exit()
# # addVoucher(..)
# tx = voucher_inst.functions.addVoucher(WEB3.eth.accounts[1], WEB3.toBytes(text="test description"), 1)\
#     .buildTransaction({'nonce': WEB3.eth.getTransactionCount(user_inst["publickeyUser"]),
#     'from': user_inst["publickeyUser"]})
# # bei einer echten Transaktion:
# #signed_tx = WEB3.eth.account.signTransaction(tx, private_key=some_account["privatekeyUser"])
# #WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
# # ganache Transaktion (unsigniert):
# WEB3.eth.sendTransaction(tx)

#
#
# # redeemVoucher(..)
# tx = voucher_inst.functions.redeem(0)\
#     .buildTransaction({'nonce': WEB3.eth.getTransactionCount(WEB3.eth.accounts[1]), 'from': WEB3.eth.accounts[1]})
# # bei einer echten Transaktion:
# #   signed_tx = WEB3.eth.account.signTransaction(tx, private_key=some_account.key)
# #   WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
# # ganache Transaktion (unsigniert):
# WEB3.eth.sendTransaction(tx)
#
#
#
#
#
# # Create a sample account
# acc = WEB3.eth.account.create()
#
# print("public key:", acc.address)
# print("private key:", acc.key)
