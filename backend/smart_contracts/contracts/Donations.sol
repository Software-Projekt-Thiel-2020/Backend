pragma solidity ^0.5.16;
/// @title SmartContract zum Verwalten von Spenden
contract Project {

    modifier onlyOwner(){
        require(msg.sender == owner);
        _;
    }

    ProjectTarget projectTarget;

    enum votePosition{POSITIVE_VOTE, NEGATIVE_VOTE}

    mapping(uint8 => Milestone) public milestones;
    mapping(address => Donor) public donors;

    uint256 donated_amount;     // Insgesamt gespendeter Betrag
    uint256 minDonation;        // min. gespendeter Betrag zum waehlen
    uint256 already_withdrawn;
    uint8 milestonesCounter = 0;
    uint8 activeMilestone;
    uint8 partial_payment;
    address owner;

    struct Milestone {
        bytes name;
        uint256 targetAmount;
        uint32 voteableUntil;
        uint32 positiveVotes;
        uint32 negativeVotes;
        bool payoutPart;
        bool payoutAll;
    }

    struct ProjectTarget {
        bytes name;
        uint256 amount;
    }

    struct Donor {
        uint256 votedMilestones;
        uint256 donated_amount;
        uint8 donated_for_milestone;
        bool wantsToVote;
        bool exists;
    }

    event PayingOutPart(uint8 milestoneId, uint256 amount);
    event PayingOutAll(uint8 milestoneId, uint256 amount);
    event Donate(uint256 amount, uint8 milestoneId, address donor_add, bool wantsToVote);
    event Donate_Light(uint256 amount);
    event Vote(uint8 milestoneId, address donor_add, votePosition vp);
    event AddMilestone(bytes _name, uint256 _amount);
    event PayingOutProject(uint256 _amount);
    event Retract(uint256 amount, uint8 milestoneId, address donor);

    /// @param _partial_payment Teilauszahlung in Prozent von 0-100
    /// @param _projectTargetName Name des Projektziels in hex
    /// @param _projectTargetAmount das Projektziels in Wei
    /// @param _minDonation Mindestbetrag einer Spende um Stimmbereichtigt zu sein
    constructor(uint8 _partial_payment, bytes memory _projectTargetName, uint256 _projectTargetAmount, uint256 _minDonation) public {
        require(_partial_payment < 100);
        require(_projectTargetName.length > 0);
        require(_projectTargetAmount > 0);

        partial_payment = _partial_payment;
        projectTarget = ProjectTarget(_projectTargetName, _projectTargetAmount);
        minDonation = _minDonation;
        owner = msg.sender;
    }

    /// @notice Fuert eine Teilauszahlung des Meilensteins aus,
    /// @notice wenn die Abstimmzeit abgelaufen ist und mehr positive als negative Stimmen gesammelt wurden
    /// @param milestoneId ID des Meilensteins der ausgezahlt werden soll
    function payingOutActiveMilestonePart(uint8 milestoneId) onlyOwner public {
        Milestone memory m = milestones[milestoneId];
        require(m.payoutPart == false);
        require(m.payoutAll == false);
        require(m.voteableUntil <= block.timestamp);
        require(m.positiveVotes > m.negativeVotes);

        uint256 amount;
        if (milestoneId > 0) {
            amount = ((m.targetAmount - already_withdrawn) / 100) * partial_payment;
        } else {
            amount = (m.targetAmount / 100) * partial_payment;
        }

        if (amount > address(this).balance) {
            amount = address(this).balance;
        }

        already_withdrawn += amount;
        msg.sender.transfer(amount);
        m.payoutPart = true;

        milestones[milestoneId] = m;
        activeMilestone++;

        emit PayingOutPart(milestoneId, amount);
    }

    /// @notice Fuert eine volle Auszahlung des Meilensteins aus, wenn das Spendenziel erreicht wurde
    /// @param milestoneId ID des Meilensteins der ausgezahlt werden soll
    function payingOutActiveMilestoneAll(uint8 milestoneId) onlyOwner public {
        Milestone memory m = milestones[milestoneId];
        require(m.payoutAll == false);
        require(m.targetAmount <= donated_amount);

        uint256 amount;
        if (milestoneId > 0) {
            amount = m.targetAmount - already_withdrawn;
        } else {
            amount = m.targetAmount;
        }

        if (m.payoutPart) {
            amount = amount - ((amount / 100) * partial_payment);
        }

        if (amount > address(this).balance) {
            amount = address(this).balance;
        }

        already_withdrawn += amount;
        msg.sender.transfer(amount);
        m.payoutAll = true;

        milestones[milestoneId] = m;
        activeMilestone++;

        emit PayingOutAll(milestoneId, amount);
    }

    /// @notice Auszahlung der kompletten Summe bei Erreichung des Projektziels
    function payingOutProject() onlyOwner public {
        require(projectTarget.amount <= donated_amount);
        uint256 amount = address(this).balance;

        already_withdrawn += amount;
        msg.sender.transfer(amount);

        emit PayingOutProject(amount);
    }

    /// @notice Funktion zum Abstimmen ueber Meilensteine
    /// @param milestoneId ID des Meilensteines ueber den abgestimmt werden soll
    /// @param vp Stimme für oder gegen den Meilentein als "POSITIVE_VOTE" oder  "NEGATIVE_VOTE"
    function vote(uint8 milestoneId, votePosition vp) public {
        require(milestoneId < milestonesCounter);
        require(milestones[milestoneId].voteableUntil > block.timestamp);

        if (donors[msg.sender].wantsToVote && (donors[msg.sender].votedMilestones & (1 << uint256(milestoneId)) == 0)) {
            if (vp == votePosition.POSITIVE_VOTE) {
                milestones[milestoneId].positiveVotes++;
            } else if (vp == votePosition.NEGATIVE_VOTE) {
                milestones[milestoneId].negativeVotes++;
            }

            donors[msg.sender].votedMilestones = donors[msg.sender].votedMilestones | (1 << uint256(milestoneId));

            emit Vote(milestoneId, msg.sender, vp);
        }
    }

    function register() public {
        require(!donors[msg.sender].exists);
	require(msg.sender != owner);
        Donor memory d;
        d.exists = true;
        donors[msg.sender] = d;
    }

    /// @notice Funktion zum Spenden
    /// @notice man muss sich vor dem spenden "registrieren" mit der Funktion "register()"
    /// @param _wantsToVote wenn der Spender abstimmen moechte true ansonsten false
    function donate(bool _wantsToVote) payable public {
        require(donors[msg.sender].exists);

        if (_wantsToVote) {
            require(msg.value >= minDonation);
            donors[msg.sender].wantsToVote = true;
        }

        if (donors[msg.sender].donated_for_milestone < activeMilestone) {
            donors[msg.sender].donated_amount = msg.value;
            donors[msg.sender].donated_for_milestone = activeMilestone;
        } else {
            donors[msg.sender].donated_amount += msg.value;
        }

        donated_amount += msg.value;

        emit Donate(msg.value, activeMilestone, msg.sender, _wantsToVote);
    }

    /// @notice Funktion zum Spenden ohne Moeglichkeit des zurueckziehens oder waehlens
    /// @notice diese Funktion verursacht geringere Kosten und mann muss sich nicht registrieren
    function donate_lite() payable public {
        donated_amount += msg.value;
        emit Donate_Light(msg.value);
    }

    /// @notice Funktion zum Zurückziehen der Spende
    function retract() public {
        Donor memory d = donors[msg.sender];
        require(d.exists);
        require(d.donated_for_milestone == activeMilestone);

        Milestone memory m = milestones[activeMilestone];
        require(m.payoutAll == false);
        require(m.targetAmount > donated_amount);

        if (m.voteableUntil <= block.timestamp) {
            require(m.positiveVotes < m.negativeVotes);
        }

        uint256 amount;
        if (m.payoutPart) {
            amount = d.donated_amount - ((d.donated_amount / 100) * partial_payment);
        } else {
            amount = d.donated_amount;
        }
        msg.sender.transfer(amount);

        emit Retract(amount, activeMilestone, msg.sender);

        donated_amount -= amount;
        d.donated_for_milestone = 0;
        donors[msg.sender] = d;
    }

    /// @notice fuegt neue Meilensteine hinzu
    /// @notice das Ziel des neuen Meilensteins darf nicht kleiner als das Ziel des letzten Meilensteins
    /// @param _name Name des Meilensteins in hex
    /// @param _targetAmount Spendenziel des Meilensteins
    /// @param _voteableUntil Unixtime bis zu der abgestimmt werden kann
    function addMilestone(bytes memory _name, uint256 _targetAmount, uint32 _voteableUntil) onlyOwner public {
        require(_name.length > 0);
        require(_targetAmount < projectTarget.amount);
        require(_voteableUntil >= block.timestamp + 1 days);

        if (milestonesCounter > 0) {
            require(milestones[milestonesCounter - 1].targetAmount < _targetAmount);
        }

        milestones[milestonesCounter] = Milestone(_name, _targetAmount, _voteableUntil, 0, 0, false, false);
        milestonesCounter++;

        emit AddMilestone(_name, _targetAmount);
    }
}
