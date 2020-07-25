from backend.database.db import DB_SESSION
from backend.database.model import User, Voucher, VoucherUser, Institution
from backend.resources.helpers import auth_user, check_params_int
from backend.smart_contracts.web3 import WEB3, INSTITUTION_JSON

def voucher_constructor(institution_address):
    contract = WEB3.eth.contract(address=institution_address, abi=INSTITUTION_JSON["abi"], bytecode=INSTITUTION_JSON["bytecode"])
    ctor = contract.constructor(institution_address, WEB3.eth.defaultAccount)
    tx_hash = ctor.transact()
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")
    
    return tx_receipt.contractAddress
    
def add_voucher(user_inst, institution_address, sc_address, description=b'test', expires_in_Days=5):

    contract = WEB3.eth.contract(address=sc_address, abi=INSTITUTION_JSON["abi"])
    
    tx_hash = contract.functions.addVoucher(user_inst.publickeyUser, description, expires_in_Days).buildTransaction({
        'nonce': WEB3.eth.getTransactionCount(user_inst.publickeyUser),
        'from': user_inst.publickeyUser
    })
    signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=user_inst.privatekeyUser) #use master account
    tx_raw = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_raw)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")
    processed_receipt = contract.events.newVoucher().processReceipt(tx_receipt)

    return processed_receipt[0].args._index

def redeem_voucher(user_inst, index, sc_address):
    contract = WEB3.eth.contract(address=sc_address, abi=INSTITUTION_JSON["abi"])
    
    tx_hash = contract.functions.redeem(index).buildTransaction({
        'nonce': WEB3.eth.getTransactionCount(user_inst.publickeyUser),
        'from': user_inst.publickeyUser
    })
    signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=user_inst.privatekeyUser)
    tx_raw = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_raw)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")