pragma solidity ^0.6.0;
//pragma experimental ABIEncoderV2;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";
contract Project is Ownable{
  
  //time variable -> wie verkleinert -> timestamp?
  
  //wie sinnvoll ist es geld abzuheben? -> minimum voting betrag wird sinnlos
  
  //negative votes nötig?
  
  //ToDo: wenn Zeit abgelaufen darf nicht mehr gewählt werden
  
 //ToDo: Spenden werden ausgezahlt, wenn (voting)Ziel erreicht ist und minDonation erreicht wurde? Was wenn nicht erreicht?
 // '-> project hat ein button zum auszahlen der Donor beträge (an owner). Button funktioniert nur wenn Bedingungen erreicht.
 //Geld befindet sich momentan im Donor contract, sinnvoll?
 
 //Viele Methoden noch unsicher! Jeder kann sie aufrufen -> welche? (vor allem setter)
 
 
  constructor(int _time) public{
      require(_time > 0); //  wie klein darf time sein?
      time = _time;
  }
  
  function getAddress() view public returns (address){
      return address(this);
  }
  
  mapping(uint8 => Milestone) public milestones;
  mapping(address => Donor) public donors;
  uint8 milestonesCounter = 0;

  int time; // wie lange darf noch gevoted werden? Auf Projekt oder auf Milestone bezogen?
 
  enum votePosition{ POSITIVE_VOTE, NEGATIVE_VOTE}
 
  
  struct Milestone {
    bytes name;            // muss in hex übergeben werden
    uint256 donatedAmount;  //bereits gespendet
    uint256 minDonation; //benötigte Spenden zum erreichen des Meilensteins, nicht im Pflichtenheft
    uint128 neededVotes;  //   Vom ersteller festgelegt? gibt es ein minimum?
    uint128 minDonToVote; //min. gespendeter Betrag zum wählen
    uint32 positiveVotes;
    uint32 negativeVotes;
    bool donReached;        //test
    bool votesReached;      //test
    
  }
  
  function setDonatedAmount(uint8 milestoneId,uint256 amount)public{
        milestones[milestoneId].donatedAmount += amount;
  }
  
   event Vote(uint8 milestoneId, address donor_add,votePosition vp);
  
    //ToDo: überprüfen ob der aufrufer der Donor der addresse ist! -> wie?
    // erhöht den wahl counter des projects(positiv oder negativ).
    //Problem: wenn man in remix value auf 5 ether stellt und 5 zahlt wird counter um 5 erhöht. Bei wei genau so.
    function vote(uint8 milestoneId, address donor_add,votePosition vp) public {
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
    
    
  
   event AddMilestone(bytes _name, uint256 _minDonation, uint128 _neededVotes,uint128 _minDonToVote,uint32 positiveVotes,uint32 negativeVotes);
   
   //fügt einen neuen Meilenstein hinzu. Prüft ob das Ziel höher ist als beim letzten (beim ersten nicht)
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
   
   event DonationReached(uint8 milestoneId);
   
   function checkIfDonationReached(uint8 milestoneId) public{
       if(milestones[milestoneId].donatedAmount >= milestones[milestoneId].minDonation){
           milestones[milestoneId].donReached = true;
           emit DonationReached(milestoneId);
       }
   }
   
   event VotesReached(uint8 milestoneId);
   
   function checkIfVotingReached(uint8 milestoneId) public{
       if(milestones[milestoneId].neededVotes >= milestones[milestoneId].positiveVotes){
           milestones[milestoneId].votesReached = true;
           emit VotesReached(milestoneId);
       }
   }
  
}

contract Donor is Ownable{
    
    Project project;
    
    
    //Spender mit bestimmten Projekt verbinden, er muss die Adresse (öffentlich abrufbar) des Projects eingeben
    constructor(address ProjectAddress) public{
        project = Project(ProjectAddress);
    }
    
    
    bool[128] votedMilestones; //es wird nicht gespeichert ob votes negativ sind, mapping immer besser?
    bool[128] wantsToVote;
    
    function getVotedMilestones(uint8 milestoneId) public view returns (bool){
        return votedMilestones[milestoneId];
    }
    
    function setVotedMilestones(uint8 milestoneId) public{
        votedMilestones[milestoneId] = true;
    }
    
    function getWantsToVote(uint8 milestoneId) public view returns (bool){
        return wantsToVote[milestoneId];
    }
    
    mapping(uint8 => uint256) public donatedAmountPerMilestone;
    
    function getDonatedAmountPerMilestone(uint8 milestoneId) public view returns(uint256){
        return donatedAmountPerMilestone[milestoneId];
    }
    
    function setDonatedAmountPerMilestone(uint8 milestoneId,uint256 amount) public{
        donatedAmountPerMilestone[milestoneId] += amount;
    }
    
    
    event Donate(uint256 amount, uint8 milestoneId, bool wantsToVote);
    event Withdraw(uint256 amount, uint8 milestoneId);
    
    
    
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
    
    //für bestimmten milestone spenden
    //warnen wenn nicht genug geld auf konto?
    //spenden auf nicht existierende milestones möglich
    function donateAndVote(uint256 amount,uint8 milestoneId) onlyOwner payable public {
        require(msg.value == amount);
        donatedAmountPerMilestone[milestoneId] += amount;
        project.setDonatedAmount(milestoneId, amount);
        wantsToVote[milestoneId] = true;
        emit Donate(amount,milestoneId,true);
        
    }
    
    //Laut Pflichtenheft donate methoden in project. -> kann man noch schnell ändern aber ich find das so schöner..
    //'-> sinnvoll?
    function donateDontVote(uint256 amount,uint8 milestoneId) onlyOwner payable public {
        require(msg.value == amount);
        donatedAmountPerMilestone[milestoneId] += amount;
        project.setDonatedAmount(milestoneId, amount);
        wantsToVote[milestoneId] = false;
        emit Donate(amount,milestoneId,false);
        
    }

   //bestimmten betrag von bestimmten Milestone abheben (nur wenn vorher auch so viel gespendet)
    function withdraw(uint256 amount,uint8 milestoneId) onlyOwner payable public {
        require(donatedAmountPerMilestone[milestoneId] >= amount);
        donatedAmountPerMilestone[milestoneId] -= amount;
        msg.sender.transfer(amount);
        emit Withdraw(amount, milestoneId);
        
    }
    
    //onlyOwner ??
    function getBalanceInMilestone(uint8 milestoneId) view public returns (uint256){
        return donatedAmountPerMilestone[milestoneId];
    }

     
    
}
