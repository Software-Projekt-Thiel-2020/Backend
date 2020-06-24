import configparser
from pathlib import Path

from web3 import Web3

base = Path.cwd() / "backend" / "smart_contracts"

CFG_PARSER: configparser.ConfigParser = configparser.ConfigParser()
CFG_PARSER.read("backend_config.ini")


W3: Web3 = Web3(Web3.HTTPProvider(CFG_PARSER["Ethereum"]["URI"]))


if W3.isConnected():
    print("connected to ethereum node.")
else:
    print("could not connect to ethereum node.")
    exit(1)


"""
import json
W3.eth.defaultAccount = W3.eth.accounts[0]

voucher_path = base / "build" / "contracts" / "Institution.json"

with open(str(voucher_path)) as json_file:
    voucher_json = json.load(json_file)

Voucher = W3.eth.contract(abi=voucher_json["abi"], bytecode=voucher_json["bytecode"])
tx_hash = Voucher.constructor().transact()
tx_receipt = W3.eth.waitForTransactionReceipt(tx_hash)


voucher_inst = W3.eth.contract(address=tx_receipt.contractAddress, abi=voucher_json["abi"])

# addVoucher(..)
tx = voucher_inst.functions.addVoucher(W3.eth.accounts[1], W3.toBytes(text="test description"), 1)\
    .buildTransaction({'nonce': W3.eth.getTransactionCount(W3.eth.defaultAccount)})
# bei einer echten Transaktion:
#   signed_tx = W3.eth.account.signTransaction(tx, private_key=some_account.key)
#   W3.eth.sendRawTransaction(signed_tx.rawTransaction)
# ganache Transaktion (unsigniert):
W3.eth.sendTransaction(tx)


# redeemVoucher(..)
tx = voucher_inst.functions.redeem(0)\
    .buildTransaction({'nonce': W3.eth.getTransactionCount(W3.eth.accounts[1]), 'from': W3.eth.accounts[1]})
# bei einer echten Transaktion:
#   signed_tx = W3.eth.account.signTransaction(tx, private_key=some_account.key)
#   W3.eth.sendRawTransaction(signed_tx.rawTransaction)
# ganache Transaktion (unsigniert):
W3.eth.sendTransaction(tx)





# Create a sample account
acc = W3.eth.account.create()

print("public key:", acc.address)
print("private key:", acc.key)

"""
