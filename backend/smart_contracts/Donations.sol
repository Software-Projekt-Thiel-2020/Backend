pragma solidity ^0.6.0;
// pragma experimental ABIEncoderV2;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";
contract Project is Ownable{
    
    ProjectTarget projectTarget;
    
    enum votePosition{ POSITIVE_VOTE, NEGATIVE_VOTE}
    
    mapping(uint8 => Milestone) public milestones;
    mapping(address => Donor) public donors;
    
    uint256 donated_amount;     // Insgesamt gespendeter Betrag
    uint256 minDonation;        // min. gespendeter Betrag zum waehlen -> fuer ziel und nicht fuer meilenstein?
    uint256 already_withdrawn;
    uint8 milestonesCounter = 0;
    uint8 activeMilestone;
    uint8 partial_payment;
    
    struct Milestone {
        bytes name;             // muss in hex uebergeben werden
        uint256 targetAmount;   // Ziel fuer den Meilenstein
        uint32 voteableUntil;   // Unixtime, es darf abgestimmt werden bis zu diesem Zeitpunkt
        uint32 positiveVotes;
        uint32 negativeVotes;
        bool payoutPart;
        bool payoutAll;
    }
    
    struct ProjectTarget {
        bytes name;             // muss in hex uebergeben werden
        uint256 amount;         // Ziel fuer das Projektziel
    }
  
    struct Donor {
        uint256 donated_amount;
        uint8 donated_for_milestone;
        bool[256] votedMilestones; 
        bool wantsToVote;
        bool exists;
    }
  
    event PayingOutPart(uint8 milestoneId, uint256 amount);
    event PayingOutAll(uint8 milestoneId, uint256 amount);
    event Donate(uint256 amount, uint8 milestoneId, address donor_add,bool wantsToVote);
    event Vote(uint8 milestoneId, address donor_add,votePosition vp);
    event AddMilestone(bytes _name, uint256 _amount, uint256 _minDonation,uint128 _minDonToVote,uint32 positiveVotes,uint32 negativeVotes);
    event PayingOutProject(uint256 _amount);
  
     /// @param partial_payment Teilauszahlung in Prozent von 0-100
    constructor(uint8 _partial_payment,bytes memory _projectTargetName, uint256 _projectTargetAmount) public {
        require(_partial_payment > 0);
        require(_partial_payment < 100);
        require(_projectTargetName.length > 0);
        require(_projectTargetAmount > 0);
        partial_payment =_partial_payment;
        projectTarget = ProjectTarget(_projectTargetName, _projectTargetAmount);
    }
  
    // was bei nicht existierenden milestones?
    // wenn spendenziel erreicht prozentsatz -> wie viel? 
    // wenn voting ziel erreicht alles
    function payingOutActiveMilestonePart(uint8 milestoneId) onlyOwner public {
        Milestone memory m = milestones[milestoneId];
        require(m.payoutPart == false);
        require(m.payoutAll == false);
        require(m.voteableUntil <= block.timestamp);
        require(m.positiveVotes > m.negativeVotes);
        uint256 amount;
        if(milestoneId > 0){
            amount = ((m.targetAmount - already_withdrawn) / 100) * partial_payment;
        }else{
            amount = (m.targetAmount / 100) * partial_payment ;
        }
        if(amount > address(this).balance){
            amount = address(this).balance;
        }
        already_withdrawn += amount;
        msg.sender.transfer(amount);
        m.payoutPart = true;
        milestones[milestoneId] = m;
        activeMilestone++;
        emit PayingOutPart(milestoneId,amount);
    }
    
    function payingOutActiveMilestoneAll(uint8 milestoneId) onlyOwner public {
        Milestone memory m = milestones[milestoneId];
        require(m.payoutAll == false);
        require(m.targetAmount > donated_amount);
        uint256 amount;
        if(milestoneId > 0){
            amount = m.targetAmount - already_withdrawn;
        }else{
            amount = m.targetAmount;
        }
        if(m.payoutPart){
            amount = amount - (( amount / 100 ) * partial_payment);
        }
        if(amount > address(this).balance){
            amount = address(this).balance;
        }
        already_withdrawn += amount;
        msg.sender.transfer(amount);
        m.payoutAll = true;
        milestones[milestoneId] = m;
        activeMilestone++;
        emit PayingOutAll(milestoneId,amount);
    }
    
    // wenn das Projektziel erreicht wurde darf der Besitzer jederzeit das gesamte Geld abheben
    function payingOutProject() onlyOwner public {
        require(projectTarget.amount <= donated_amount);
        uint256 amount = address(this).balance;
        already_withdrawn += amount;
        msg.sender.transfer(amount); 
        emit PayingOutProject(amount);
    }
    
    // erhoeht den wahl counter des projects(positiv oder negativ).
    function vote(uint8 milestoneId, votePosition vp) public {
        require(milestoneId<milestonesCounter);
        require(milestones[milestoneId].voteableUntil > block.timestamp);
        if(donors[msg.sender].wantsToVote
        && (donors[msg.sender].votedMilestones[milestoneId] == false)){
            if(vp == votePosition.POSITIVE_VOTE){
                milestones[milestoneId].positiveVotes++;
            } else if(vp == votePosition.NEGATIVE_VOTE){
                milestones[milestoneId].negativeVotes++;
            }
            donors[msg.sender].votedMilestones[milestoneId] = true;
            emit Vote(milestoneId,msg.sender,vp);
        }
    }    
    
    function donate(uint8 milestoneId, bool _wantsToVote) payable public {
        require(milestoneId <= activeMilestone);    // Es darf nur maximal auf den aktuellen Meilenstein gespendet werden 
        Donor memory d;
        d=donors[msg.sender];
        if(_wantsToVote){
            require(msg.value >= minDonation);
            d.wantsToVote = true;
        }else{
            d.wantsToVote = false;
        }
        if(d.exists){
            if(d.donated_for_milestone < activeMilestone){
                d.donated_amount = msg.value;
                d.donated_for_milestone = activeMilestone;
            }else{
               d.donated_amount += msg.value; 
            }
        }else{
            d.donated_amount = msg.value;
            d.donated_for_milestone = activeMilestone;
            d.exists = true;
        }
        donated_amount += msg.value;
        donors[msg.sender]=d;
        emit Donate(msg.value, activeMilestone, msg.sender, _wantsToVote);
    }
  
    // Meilensteine duerfen  nicht kleiner als der bis dahin hoechste Meilenstein sein
    function addMilestone(bytes memory _name,uint _amount, uint256 _minDonation,uint128 _minDonToVote, uint32 _voteableUntil) onlyOwner public {
        require(_name.length > 0);
        require(_amount < projectTarget.amount);
        require(_voteableUntil >= block.timestamp + 1 days);
        if(milestonesCounter>0){
            require(milestones[milestonesCounter].targetAmount < _amount);
        }
        milestones[milestonesCounter] = Milestone(_name,_amount,_voteableUntil,0,0,false,false);
        milestonesCounter ++;
        emit AddMilestone(_name,_amount,_minDonation,_minDonToVote,0,0);
    }
}
