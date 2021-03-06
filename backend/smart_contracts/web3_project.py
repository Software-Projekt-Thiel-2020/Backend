import time
from typing import Optional

from backend.database.model import User, Project, Donation
from backend.smart_contracts.web3 import WEB3, PROJECT_JSON


def project_constructor(owner: User, description: str, goal: int):
    projects_sc = WEB3.eth.contract(abi=PROJECT_JSON["abi"], bytecode=PROJECT_JSON["bytecode"])

    description_bytes = WEB3.toBytes(text=str(description))

    # constructor(_owner, _admin, _partial_payment, _projectTargetName, _projectTargetAmount, _minDonation)
    ctor = projects_sc.constructor(owner.publickeyUser, WEB3.eth.defaultAccount,
                                   80,
                                   description_bytes,
                                   goal,
                                   int(WEB3.toWei(0.01, 'ether')))
    tx_hash = ctor.buildTransaction({'nonce': WEB3.eth.getTransactionCount(owner.publickeyUser),
                                     'from': owner.publickeyUser})
    signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=owner.privatekeyUser)
    tx_hash = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")

    return tx_receipt.contractAddress


def project_constructor_check(owner: User, description: str, goal: int):
    # require(_partial_payment < 100);

    if not len(description) > 0:  # require(_projectTargetName.length > 0);
        return "description needed", 0

    if not goal > 0:  # require(_projectTargetAmount > 0);
        return "goal needs to be a positive number", 0

    try:
        projects_sc = WEB3.eth.contract(abi=PROJECT_JSON["abi"], bytecode=PROJECT_JSON["bytecode"])
        description_bytes = WEB3.toBytes(text=str(description))
        ctor = projects_sc.constructor(owner.publickeyUser, WEB3.eth.defaultAccount,
                                       80,
                                       description_bytes,
                                       goal,
                                       int(WEB3.toWei(0.01, 'ether')))
        transaction = ctor.buildTransaction({'nonce': WEB3.eth.getTransactionCount(owner.publickeyUser),
                                             'from': owner.publickeyUser})
        price = transaction["gasPrice"] * transaction["gas"]
        if price >= WEB3.eth.getBalance(owner.publickeyUser):
            return "not enough balance", 0
    except ValueError:
        return "balance check failed (can be bad params!)", 0

    return None, price


def project_add_milestone(project: Project, owner: User, name: str, goal: int, until: int):
    projects_sc = WEB3.eth.contract(address=project.scAddress, abi=PROJECT_JSON["abi"])

    tx_hash = projects_sc.functions.addMilestone(WEB3.toBytes(text=name),
                                                 int(goal),
                                                 int(until)). \
        buildTransaction({'nonce': WEB3.eth.getTransactionCount(owner.publickeyUser),
                          'from': owner.publickeyUser})
    signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=owner.privatekeyUser)
    tx_hash = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)

    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash)
    if tx_receipt.status != 1:
        raise RuntimeError("SC addMilestone Call failed!")

    processed_receipt = projects_sc.events.AddMilestone().processReceipt(tx_receipt)
    if len(processed_receipt) < 1:
        raise RuntimeError("SC addMilestone no Events")
    if WEB3.toText(processed_receipt[0].args._name) != name:  # pylint:disable=protected-access
        raise RuntimeError("SC addMilestone Event name wrong!")
    if processed_receipt[0].args._amount != goal:  # pylint:disable=protected-access
        raise RuntimeError("SC addMilestone Event goal wrong!")

    return processed_receipt[0].args.milestone_id


# pylint:disable=too-many-arguments
def project_add_milestone_check(session, project: Project, owner: User, name: str, goal: int, until: int):
    if not len(name) > 0:  # require(_name.length > 0);
        return "description needed", 0

    if not goal < project.goal:  # require(_targetAmount < projectTarget.amount);
        return "milestone goal greater than project goal", 0

    if not until >= (int(time.time()) + 60 * 60 * 24):  # require(_voteableUntil >= block.timestamp + 1 days);
        return "until needs to be at least 1 day in the future!", 0
    if until > 2**64:
        return "milestone until value is not a valid date... or is it after the 04.12.219250468 15:30:07 already?!", 0

    # require(milestones[milestonesCounter - 1].targetAmount < _targetAmount);
    for milestone in project.milestones:
        if not milestone.goalMilestone < goal:
            return "milestone goal smaller than existing milestone", 0
    if owner:
        pass

    sample_project = session.query(Project).get(1).scAddress  # hacky, but works
    try:
        projects_sc = WEB3.eth.contract(address=sample_project, abi=PROJECT_JSON["abi"])

        transaction = projects_sc.functions.addMilestone(WEB3.toBytes(text=name),
                                                         WEB3.toWei(99999999998, 'ether'),
                                                         int(until)). \
            buildTransaction({'nonce': WEB3.eth.getTransactionCount(WEB3.eth.defaultAccount),
                              'from': WEB3.eth.defaultAccount})
        price = transaction["gasPrice"] * transaction["gas"]
    except ValueError:
        return "balance check failed (can be bad params!)", 0

    return None, price


def project_donate_register(project: Project, user_inst: User):
    donations_sc = WEB3.eth.contract(address=project.scAddress, abi=PROJECT_JSON["abi"])

    tx_hash = donations_sc.functions.register().buildTransaction({
        'nonce': WEB3.eth.getTransactionCount(user_inst.publickeyUser),
        'from': user_inst.publickeyUser
    })
    signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=user_inst.privatekeyUser)
    tx_hash2 = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash2)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")


def project_donate_register_check(project: Project, user_inst: User) -> Optional[str]:
    if not user_inst.publickeyUser != project.institution.user.publickeyUser:  # require(msg.sender != owner);
        return "owner can't donate"

    return None


def project_donate(project: Project, user_inst: User, amount: int, vote_enabled: bool):
    project_donate_register(project, user_inst)

    donations_sc = WEB3.eth.contract(address=project.scAddress, abi=PROJECT_JSON["abi"])

    tx_hash = donations_sc.functions.donate(bool(vote_enabled)) \
        .buildTransaction(
        {'nonce': WEB3.eth.getTransactionCount(user_inst.publickeyUser),
         'from': user_inst.publickeyUser, 'value': int(amount)})
    signed_tx = WEB3.eth.account.sign_transaction(tx_hash, private_key=user_inst.privatekeyUser)
    tx_hash2 = WEB3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash2)
    if tx_receipt.status != 1:
        raise RuntimeError("SC Call failed!")

    processed_receipt = donations_sc.events.Donate().processReceipt(tx_receipt)
    milestone_sc_index = processed_receipt[0].args.milestoneId  # pylint:disable=protected-access

    return milestone_sc_index


def project_donate_check(project: Project, user_inst: User, amount: int, vote_enabled: bool) -> Optional[str]:
    reg_check = project_donate_register_check(project, user_inst)
    if reg_check:
        return reg_check

    # require(donors[msg.sender].exists); - cant check

    if vote_enabled:
        if not amount > int(WEB3.toWei(0.01, 'ether')):  # require(msg.value >= minDonation);
            return "amount too low to vote"

    # cost donate_register = 1006360000000000
    # cost project_donate >1215500000000000, using factor of 2 as a safety margin (unit tests work without the margin)
    # it's not possible to estimate the donate(..) cost before registerung ;(
    if (2 * 1215500000000000 + 1006360000000000) >= WEB3.eth.getBalance(user_inst.publickeyUser):
        return "not enough balance"

    return None


def project_donate_vote(user_inst: User, vote: int, donation: Donation):
    """Method to make the voting Transaction."""
    donation_sc = WEB3.eth.contract(address=donation.milestone.project.scAddress, abi=PROJECT_JSON["abi"])

    transaction = donation_sc.functions.vote(donation.milestone.milestone_sc_id, vote)
    transaction = transaction.buildTransaction({'nonce': WEB3.eth.getTransactionCount(user_inst.publickeyUser),
                                                'from': user_inst.publickeyUser})
    signed_transaction = WEB3.eth.account.sign_transaction(transaction, user_inst.privatekeyUser)

    tx_hash = WEB3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    tx_receipt = WEB3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt


def project_donate_vote_check(user_inst: User, vote: int, donation: Donation) -> Optional[str]:
    # require(milestoneId < milestonesCounter); - invariant

    # require(milestones[milestoneId].voteableUntil > block.timestamp);
    if not donation.milestone.untilBlockMilestone > int(time.time()):
        return "voting expired"

    # require(donors[msg.sender].votedMilestones & (1 << uint256(milestoneId)) == 0); - invariant

    # require(donors[msg.sender].wantsToVote);
    if not donation.voteDonation:
        return "didnt register for voting"

    try:
        donation_sc = WEB3.eth.contract(address=donation.milestone.project.scAddress, abi=PROJECT_JSON["abi"])

        transaction = donation_sc.functions.vote(donation.milestone.milestone_sc_id, vote)
        transaction = transaction.buildTransaction({'nonce': WEB3.eth.getTransactionCount(user_inst.publickeyUser),
                                                    'from': user_inst.publickeyUser})
        price = transaction["gasPrice"] * transaction["gas"]
        if price >= WEB3.eth.getBalance(user_inst.publickeyUser):
            return "not enough balance"
    except ValueError:
        return "balance check failed (can be bad params!)"

    return None
