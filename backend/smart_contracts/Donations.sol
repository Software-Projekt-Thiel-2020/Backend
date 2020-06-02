pragma solidity ^0.6.0;
// pragma experimental ABIEncoderV2;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";
contract Project is Ownable{
  
    // anstatt import ownable eigenen modifier?  
  
    // wenn man geld abhebt darf man eventuell nicht mehr voten
  
    // man spendet fuer Ziel nicht fuer milestone.
    
    // Viele Methoden noch unsicher! Jeder kann sie aufrufen -> welche? (vor allem setter)
 
    
    // @param partial_payment in Prozent von 0-100
    constructor(uint8 _partial_payment) public {
        require(_partial_payment>0);
        require(_partial_payment<100);
        partial_payment=_partial_payment;
    }
  
    mapping(uint8 => Milestone) public milestones;
    mapping(address => Donor) public donors;
    uint8 milestonesCounter = 0;
    
    uint time;                  // wie lange darf noch gevoted werden? Auf Projekt oder auf Milestone bezogen?
    uint256 donated_amount;     // Insgesamt gespendeter Betrag
    uint256 minDonation;        // min. gespendeter Betrag zum waehlen -> fuer ziel und nicht fuer meilenstein?
    uint256 already_withdrawn;
    uint8 activeMilestone;
    uint8 partial_payment;
 
    enum votePosition{ POSITIVE_VOTE, NEGATIVE_VOTE}
    
    struct Milestone {
        bytes name;             // muss in hex uebergeben werden
        uint256 targetAmount;   // Ziel fuer den Meilenstein
        uint32 voteableUntil;   // Unixtime, es darf abgestimmt werden bis zu diesem Zeitpunkt
        uint32 positiveVotes;
        uint32 negativeVotes;
        bool payoutPart;
        bool payoutAll;
    }
  
    event PayingOutPart(uint8 milestoneId,uint amount);
    event PayingOutAll(uint8 milestoneId);
    event Donate(uint256 amount, uint8 milestoneId, address donor_add,bool wantsToVote);
    event Vote(uint8 milestoneId, address donor_add,votePosition vp);
    event AddMilestone(bytes _name, uint256 _amount, uint256 _minDonation,uint128 _minDonToVote,uint32 positiveVotes,uint32 negativeVotes);
  
    function getAddress() view public returns (address){
        return address(this);
    }
  
    // was bei nicht existierenden milestones?
    // wenn spendenziel erreicht prozentsatz -> wie viel? 
    // wenn voting ziel erreicht alles
    function payingOutActiveMilestone(uint8 milestoneId) onlyOwner public {
        if(milestones[milestoneId].positiveVotes < milestones[milestoneId].negativeVotes){
            if(donated_amount >= milestones[milestoneId].targetAmount && (milestones[milestoneId].payoutPart == false)){
                uint256 amount= ((milestones[milestoneId].targetAmount - milestones[milestoneId-1].targetAmount) * partial_payment)/100;  // partial_payment auszahlen;
                msg.sender.transfer(amount);                 
                milestones[milestoneId].payoutPart = true;
                emit PayingOutPart(milestoneId,amount);
        }
        } else if(milestones[milestoneId].positiveVotes >= milestones[milestoneId].negativeVotes && (milestones[milestoneId].payoutAll == false)){
            uint256 amount= (milestones[milestoneId].targetAmount - milestones[milestoneId-1].targetAmount);  // partial_payment auszahlen;
            if(milestones[milestoneId].payoutPart){
                amount=amount - ((amount* partial_payment)/100);
            }
            msg.sender.transfer(amount);
            milestones[milestoneId].payoutPart = true;
            milestones[milestoneId].payoutAll = true;
            emit PayingOutAll(milestoneId);
        }
    }
  

  
    // if durch require ersetzen?  
    // ToDo: ueberpruefen ob der aufrufer der Donor der addresse ist! -> wie?
    // erhoeht den wahl counter des projects(positiv oder negativ).
    // Problem: wenn man in remix value auf 5 ether stellt und 5 zahlt wird counter um 5 erhoeht. Bei wei genau so.
    function vote(uint8 milestoneId, address donor_add,votePosition vp) public {
        require(time>now);
        if(donors[donor_add].getWantsToVote(milestoneId) 
        && (donors[donor_add].getVotedMilestones(milestoneId) == false)){
            if(vp == votePosition.POSITIVE_VOTE){
                milestones[milestoneId].positiveVotes++;
            } else if(vp == votePosition.NEGATIVE_VOTE){
                milestones[milestoneId].negativeVotes++;
            }
            donors[donor_add].setVotedMilestones(milestoneId);
            emit Vote(milestoneId,donor_add,vp);
        }
    }    
    
    // fuer bestimmten milestone spenden
    // spenden auf nicht existierende milestones moeglich
    // wer kann diese Funktion aufrufen?
    function donateAndVote(uint8 milestoneId,address donor_add) onlyOwner payable public {
        donors[donor_add].setDonatedAmountPerMilestone(milestoneId,msg.value);
        donated_amount += msg.value;
        donors[donor_add].setWantsToVote(milestoneId);
        emit Donate(msg.value,milestoneId,donor_add,true);
        
    }
    
    function donateDontVote(uint8 milestoneId,address donor_add) onlyOwner payable public {
        donors[donor_add].setDonatedAmountPerMilestone(milestoneId,msg.value);
        donated_amount += msg.value;
        emit Donate(msg.value,milestoneId,donor_add,false);
    }
  
    // Meilensteine duerfen kleiner ausfallen als das Projektziel aber nicht kleiner als der bis dahin hoechste Meilenstein
    function addMilestone(bytes memory _name,uint _amount, uint256 _minDonation,uint128 _minDonToVote, uint32 _voteableUntil) onlyOwner public {
        require (_name.length > 0);
        if(milestonesCounter>0){
            require(milestones[milestonesCounter].targetAmount < _amount);
        }
        milestones[milestonesCounter] = Milestone(_name,_amount,_voteableUntil,0,0,false,false);
        milestonesCounter ++;
        emit AddMilestone(_name,_amount,_minDonation,_minDonToVote,0,0);
    }
}

contract Donor is Ownable{
    
    Project project;
    
    
    // Spender mit bestimmten Projekt verbinden, er muss die Adresse (oeffentlich abrufbar) des Projects eingeben
    constructor(address ProjectAddress) public{
        project = Project(ProjectAddress);
    }
    
    mapping(uint8 => uint256) public donatedAmountPerMilestone;

    bool[128] votedMilestones; // mapping immer besser?
    bool[128] wantsToVote;
    
    event Withdraw(uint256 amount, uint8 milestoneId);
    
    function getVotedMilestones(uint8 milestoneId) public view returns (bool) {
        return votedMilestones[milestoneId];
    }
    
    function setVotedMilestones(uint8 milestoneId) public {
        votedMilestones[milestoneId] = true;
    }
    
    function getWantsToVote(uint8 milestoneId) public view returns (bool) {
        return wantsToVote[milestoneId];
    }
    
    function setWantsToVote(uint8 milestoneId)public {
        wantsToVote[milestoneId] = true;
    }

    function getDonatedAmountPerMilestone(uint8 milestoneId) public view returns(uint256) {
        return donatedAmountPerMilestone[milestoneId];
    }
    
    function setDonatedAmountPerMilestone(uint8 milestoneId,uint256 amount) public {
        donatedAmountPerMilestone[milestoneId] += amount;
    }
    
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    // bestimmten betrag von bestimmten Milestone abheben (nur wenn vorher auch so viel gespendet)
    function withdraw(uint256 amount,uint8 milestoneId) onlyOwner payable public {
        require(donatedAmountPerMilestone[milestoneId] >= amount);
        donatedAmountPerMilestone[milestoneId] -= amount;
        msg.sender.transfer(amount);
        emit Withdraw(amount, milestoneId);
        
    }
    
    // onlyOwner ??
    function getBalanceInMilestone(uint8 milestoneId) view public returns (uint256) {
        return donatedAmountPerMilestone[milestoneId];
    }
}
