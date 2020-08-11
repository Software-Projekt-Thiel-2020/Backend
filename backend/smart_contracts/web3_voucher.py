from datetime import datetime
from typing import Optional

from backend.database.model import Institution, User, VoucherUser
from backend.smart_contracts.web3 import WEB3, INSTITUTION_JSON


def voucher_constructor(institution_owner_address):
    """
    Calls the voucher constructor for the given institution.
    :parameter institution_owner_address wallet address on the blockchain
    :return: the address of the deployed contract
    """
    # web3 default account is used for this:
    donations_contract = WEB3.eth.contract(abi=INSTITUTION_JSON["abi"], bytecode=INSTITUTION_JSON["bytecode"])
    ctor = donations_contract.constructor(institution_owner_address, WEB3.eth.defaultAccount)
    tx_hash = ctor.transact()
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash)
    if tx_receipt.status != 1:
        raise RuntimeError("SC voucher ctor failed!")

    return tx_receipt.contractAddress


def voucher_constructor_check(institution_owner_address) -> Optional[str]:
    if not WEB3.isAddress(institution_owner_address):
        return "invalid public key"

    return None


def add_voucher(user: User, institution: Institution, description, expires):
    """
    Creates a new voucher for the given user.
    :parameter user the user instance who will retrieve an voucher
    :parameter institution the institution instance which offer the voucher
    :parameter description a description for the voucher
    :parameter expires the period of validity in days
    :return: the index of the created voucher
    """
    description = WEB3.toBytes(text=description)
    contract = WEB3.eth.contract(address=institution.scAddress, abi=INSTITUTION_JSON["abi"])
    tx_hash = contract.functions.addVoucher(user.publickeyUser, description, expires).buildTransaction({
        'nonce': WEB3.eth.getTransactionCount(WEB3.eth.defaultAccount),
        'from': WEB3.eth.defaultAccount
    })
    # signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=master_key)
    # tx_raw = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_raw = WEB3.eth.sendTransaction(tx_hash)
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_raw)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")

    processed_receipt = contract.events.newVoucher().processReceipt(tx_receipt)
    index = processed_receipt[0].args._index  # pylint:disable=protected-access
    print(index)
    return index


def add_voucher_check(user: User, institution: Institution, description, expires) -> Optional[str]:
    if not expires > 0:
        return "expiration cant be negative"

    try:
        description = WEB3.toBytes(text=description)
        contract = WEB3.eth.contract(address=institution.scAddress, abi=INSTITUTION_JSON["abi"])
        transaction = contract.functions.addVoucher(user.publickeyUser, description, expires).buildTransaction({
            'nonce': WEB3.eth.getTransactionCount(WEB3.eth.defaultAccount),
            'from': WEB3.eth.defaultAccount
        })
        price = transaction["gasPrice"] * transaction["gas"]
        if price > WEB3.eth.getBalance(user.publickeyUser):
            return "not enough balance"
    except ValueError:
        return "balance check failed (can be bad params!)"

    return None


def redeem_voucher(user: User, voucher_user: VoucherUser, sc_address):
    """
    Redeems a voucher.
    :parameter user the user instance who will redeem a voucher
    :parameter voucher_user the VoucherUser instance who will redeem a voucher
    :parameter sc_address the contract address where the voucher is bound
    :return: -
    """
    contract = WEB3.eth.contract(address=sc_address, abi=INSTITUTION_JSON["abi"])
    tx_hash = contract.functions.redeem(voucher_user.redeem_id).buildTransaction({
        'nonce': WEB3.eth.getTransactionCount(user.publickeyUser),
        'from': user.publickeyUser
    })
    signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=user.privatekeyUser)
    tx_raw = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_raw)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")

    processed_receipt = contract.events.redeemVoucher().processReceipt(tx_receipt)
    if len(processed_receipt) < 1:
        raise RuntimeError("SC redeem no Events")
    if processed_receipt[0].args._owner != user.publickeyUser:  # pylint:disable=protected-access
        raise RuntimeError("SC redeem Event owner wrong!")
    if processed_receipt[0].args._index != voucher_user.redeem_id:  # pylint:disable=protected-access
        raise RuntimeError("SC redeem Event index wrong!")


def redeem_voucher_check(user: User, voucher_user: VoucherUser, sc_address) -> Optional[str]:
    # require(voucher[msg.sender].length > _index); - invariant

    # require(v.used == false);
    if voucher_user.usedVoucher is not False:
        return "already used voucher"

    # require(v.expires_unixtime >= block.timestamp);
    if not voucher_user.expires_unixtime >= datetime.now():
        return "voucher is expired"

    if not WEB3.isAddress(sc_address):
        return "invalid sc_address"

    if user:
        pass

    return None
