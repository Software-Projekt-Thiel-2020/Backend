import configparser
import sys

from web3 import Web3


CFG_PARSER: configparser.ConfigParser = configparser.ConfigParser()
CFG_PARSER.read("backend_config.ini")


WEB3: Web3 = Web3(Web3.HTTPProvider(CFG_PARSER["Ethereum"]["URI"]))


if WEB3.isConnected():
    print("connected to ethereum node.")
else:
    print("could not connect to ethereum node.")
    sys.exit(1)


# import json
# from pathlib import Path
# WEB3.eth.defaultAccount = WEB3.eth.accounts[0]
#
# base = Path.cwd() / "backend" / "smart_contracts"
# voucher_path = base / "build" / "contracts" / "Institution.json"
#
# with open(str(voucher_path)) as json_file:
#     voucher_json = json.load(json_file)
#
# Voucher = WEB3.eth.contract(abi=voucher_json["abi"], bytecode=voucher_json["bytecode"])
# tx_hash = Voucher.constructor().transact()
# tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash)
#
#
# voucher_inst = WEB3.eth.contract(address=tx_receipt.contractAddress, abi=voucher_json["abi"])
#
# # addVoucher(..)
# tx = voucher_inst.functions.addVoucher(WEB3.eth.accounts[1], WEB3.toBytes(text="test description"), 1)\
#     .buildTransaction({'nonce': WEB3.eth.getTransactionCount(WEB3.eth.defaultAccount)})
# # bei einer echten Transaktion:
# #   signed_tx = WEB3.eth.account.signTransaction(tx, private_key=some_account.key)
# #   WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
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
