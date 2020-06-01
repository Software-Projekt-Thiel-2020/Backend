pragma solidity ^0.6.0;
// pragma experimental ABIEncoderV2;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";
contract Project is Ownable{
  
    // time variable -> wie verkleinert -> timestamp?
  
    // wie sinnvoll ist es geld abzuheben? -> minimum voting betrag wird sinnlos
  
    // negative votes nötig?
 
    // Viele Methoden noch unsicher! Jeder kann sie aufrufen -> welche? (vor allem setter)
 
 
    constructor(int _time) public {
        require(_time > 0); // wie klein darf time sein?
        time = _time;
    }
  
    mapping(uint8 => Milestone) public milestones;
    mapping(address => Donor) public donors;
    uint8 milestonesCounter = 0;

    int time;   // wie lange darf noch gevoted werden? Auf Projekt oder auf Milestone bezogen?
 
    enum votePosition{ POSITIVE_VOTE, NEGATIVE_VOTE}
    
    struct Milestone {
        bytes name;             // muss in hex übergeben werden
        uint256 donatedAmount;  // bereits gespendet
        uint256 minDonation;    // benötigte Spenden zum erreichen des Meilensteins, nicht im Pflichtenheft
        uint128 neededVotes;    // Vom ersteller festgelegt? gibt es ein minimum?
        uint128 minDonToVote;   // min. gespendeter Betrag zum wählen
        uint32 positiveVotes;
        uint32 negativeVotes;
        bool payoutPart;
        bool payoutAll;
    }
  
    event PayingOutPart(uint8 milestoneId,uint amount);
    event PayingOutAll(uint8 milestoneId);
    event Donate(uint256 amount, uint8 milestoneId, address donor_add,bool wantsToVote);
    event Vote(uint8 milestoneId, address donor_add,votePosition vp);
    event AddMilestone(bytes _name, uint256 _minDonation, uint128 _neededVotes,uint128 _minDonToVote,uint32 positiveVotes,uint32 negativeVotes);
  
    function getAddress() view public returns (address){
        return address(this);
    }
  
    // was bei nicht existierenden milestones?
    // wenn spendenziel erreicht prozentsatz -> wie viel? 
    // wenn voting ziel erreicht alles
    function payingOut(uint8 milestoneId) onlyOwner public {
        if(milestones[milestoneId].neededVotes < milestones[milestoneId].positiveVotes){
            if(milestones[milestoneId].donatedAmount >= milestones[milestoneId].minDonation && (milestones[milestoneId].payoutPart == false)){
                uint amount = milestones[milestoneId].donatedAmount /10;  // 10% auszahlen
                msg.sender.transfer(amount);                 
                milestones[milestoneId].donatedAmount -= amount;
                milestones[milestoneId].payoutPart = true;
                emit PayingOutPart(milestoneId,amount);
        }
        } else if(milestones[milestoneId].neededVotes >= milestones[milestoneId].positiveVotes && (milestones[milestoneId].payoutAll == false)){
            msg.sender.transfer(milestones[milestoneId].donatedAmount);
            milestones[milestoneId].payoutPart = true;
            milestones[milestoneId].payoutAll = true;
            emit PayingOutAll(milestoneId);
        }
    }
  

  
    // if durch require ersetzen?  
    // ToDo: überprüfen ob der aufrufer der Donor der addresse ist! -> wie?
    // erhöht den wahl counter des projects(positiv oder negativ).
    // Problem: wenn man in remix value auf 5 ether stellt und 5 zahlt wird counter um 5 erhöht. Bei wei genau so.
    function vote(uint8 milestoneId, address donor_add,votePosition vp) public {
        require(time>0);
        if(donors[donor_add].getWantsToVote(milestoneId) && (donors[donor_add].getDonatedAmountPerMilestone(milestoneId) >= milestones[milestoneId].minDonation) 
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
    
    // für bestimmten milestone spenden
    // spenden auf nicht existierende milestones möglich
    // wer kann diese Funktion aufrufen?
    function donateAndVote(uint8 milestoneId,address donor_add) onlyOwner payable public {
        donors[donor_add].setDonatedAmountPerMilestone(milestoneId,msg.value);
        milestones[milestoneId].donatedAmount += msg.value;
        donors[donor_add].setWantsToVote(milestoneId);
        emit Donate(msg.value,milestoneId,donor_add,true);
        
    }
    
    function donateDontVote(uint8 milestoneId,address donor_add) onlyOwner payable public {
        donors[donor_add].setDonatedAmountPerMilestone(milestoneId,msg.value);
        milestones[milestoneId].donatedAmount += msg.value;
        donors[donor_add].setWantsToVote(milestoneId);
        emit Donate(msg.value,milestoneId,donor_add,false);
    }
  
    // fügt einen neuen Meilenstein hinzu. Prüft ob das Ziel höher ist als beim letzten (beim ersten nicht)
    // um wie viel muss es größer sein?
    function addMilestone(bytes memory _name, uint256 _minDonation, uint128 _neededVotes,uint128 _minDonToVote) onlyOwner public {
        if (_name.length != 0) {
            if(milestonesCounter == 0){
                milestones[milestonesCounter] = Milestone(_name,0,_minDonation,_neededVotes,_minDonToVote,0,0,false,false);
                milestonesCounter ++;
                emit AddMilestone(_name,_minDonation,_neededVotes,_minDonToVote,0,0);
            }else if(milestones[milestonesCounter].minDonation < _minDonation)
                milestones[milestonesCounter] = Milestone(_name,0,_minDonation,_neededVotes,_minDonToVote,0,0,false,false);
                milestonesCounter ++;
                emit AddMilestone(_name,_minDonation,_neededVotes,_minDonToVote,0,0);
        }
    }
}


contract Donor is Ownable{
    
    Project project;
    
    
    // Spender mit bestimmten Projekt verbinden, er muss die Adresse (öffentlich abrufbar) des Projects eingeben
    constructor(address ProjectAddress) public{
        project = Project(ProjectAddress);
    }
    
    mapping(uint8 => uint256) public donatedAmountPerMilestone;

    bool[128] votedMilestones; //es wird nicht gespeichert ob votes negativ sind, mapping immer besser?
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