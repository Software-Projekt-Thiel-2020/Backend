
from backend.database.model import Institution, User
from backend.smart_contracts.web3 import WEB3, INSTITUTION_JSON


def voucher_constructor(institution_address):
    """
    Calls the voucher constructor for the given institution.
    :parameter institution_address wallet address on the blockchain
    :return: the address of the deployed contract
    """
    contract = WEB3.eth.contract(
        address=institution_address, abi=INSTITUTION_JSON["abi"], bytecode=INSTITUTION_JSON["bytecode"])
    ctor = contract.constructor(institution_address, WEB3.eth.defaultAccount)
    tx_hash = ctor.transact()
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")

    return tx_receipt.contractAddress


def add_voucher(user:  User, institution: Institution, description, expires):
    """
    Creates a new voucher for the given user.
    :parameter user the user instance who will retrieve an voucher
    :parameter institution the institution instance which offer the voucher
    :parameter description a description for the voucher
    :parameter expires the period of validity in days
    :return: the index of the created voucher
    """
    # TODO get master key elsewhere
    master_key = WEB3.toBytes(hexstr='e5ca8f76cb60c5fb0e35ff69622d8697c32886c768c8c59b558f63260c52ac68')

    description = WEB3.toBytes(text=description)
    contract = WEB3.eth.contract(address=institution.scAddress_voucher, abi=INSTITUTION_JSON["abi"])
    tx_hash = contract.functions.addVoucher(user.publickeyUser, description, expires).buildTransaction({
        'nonce': WEB3.eth.getTransactionCount(WEB3.eth.defaultAccount),
        'from': WEB3.eth.defaultAccount
    })
    signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=master_key)
    tx_raw = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_raw)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")

    processed_receipt = contract.events.newVoucher().processReceipt(tx_receipt)
    index = processed_receipt[0].args._index
    print(index)
    return index


def redeem_voucher(user, index, sc_address):
    """
    Redeems a voucher.
    :parameter user the user instance who will redeem a voucher
    :parameter index the voucher index
    :parameter sc_address the contract address where the voucher is bound
    :return: -
    """
    contract = WEB3.eth.contract(address=sc_address, abi=INSTITUTION_JSON["abi"])
    tx_hash = contract.functions.redeem(index).buildTransaction({
        'nonce': WEB3.eth.getTransactionCount(user.publickeyUser),
        'from': user.publickeyUser
    })
    signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=user.privatekeyUser)
    tx_raw = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_raw)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")
