pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";
contract Project is Ownable{
  
  //time variable -> wie verkleinert -> timestamp?
  
  //donor als datenstruktur damit project seine donor kennt.
  
  //wie sinnvoll ist es geld abzuheben? -> minimum voting betrag wird sinnlos
  
  //gas requirement infinite?
  
  //negative votes nötig?
  
  //wenn Zeit abgelaufen darf nicht mehr gewählt werden
  
  //donor pro Milestone entscheiden ob er voten möchte (kann er nicht mehr ändern!)
  
  //voting methode lieber in project als in donor!
  
 //Fehlt: Spenden werden ausgezahlt, wenn (voting)Ziel erreicht ist und minDonation erreicht wurde? Was wenn nicht erreicht?
 // '-> project hat ein button zum auszahlen der Donor beträge. Button funktioniert nur wenn Bedingungen erreicht.
 
 
 
  constructor(int _time) public{
      require(_time > 0); //  wie klein darf time sein?
      time = _time;
  }
  
  function getAddress() view public returns (address){
      return address(this);
  }
  
  mapping(uint8 => Milestone) public milestones;
  uint8 milestonesCounter = 0;

  int time; // wie lange darf noch gevoted werden? Auf Projekt oder auf Milestone bezogen?
  
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
  
    //getter und setter um sie im donor contract zu benutzen
  function getMilestoneMinDonToVote(uint8 _milestoneId) view public returns (uint256){
      return milestones[_milestoneId].minDonToVote;
  }
  
  //kann von jedem aufgerufen werden
  function setDonatedAmount(uint8 milestoneId, uint256 amount) external{
      milestones[milestoneId].donatedAmount += amount;
  }
  
  //kann von jedem (auch owner) aufgerufen werden!!
  function setMilestoneVotePositive(uint8 _milestoneId) external {
     
        milestones[_milestoneId].positiveVotes += 1;
      
  }
  function setMilestoneVoteNegative(uint8 _milestoneId) external {
        milestones[_milestoneId].negativeVotes += 1;
      
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
    
    
    //Spender mit bestimmten Projekt verbinden, er muss die Adresse (öffentlich abrufbar) des Projects eingeben und ob er wählen möchte.
    //'-> ob er wählen möchte wird in project verschoben
    constructor(address ProjectAddress, bool _wantsToVote) public{
        project = Project(ProjectAddress);
        wantsToVote = _wantsToVote;
    }
    
    enum votePosition{ POSITIVE_VOTE, NEGATIVE_VOTE} 
    bool[128] votedMilestones; //es wird nicht gespeichert ob votes negativ sind
    bool wantsToVote; //wird entfertn

    
    mapping(uint128 => uint256) public donatedAmountPerMilestone;
    
    event Deposit(uint256 amount, uint8 milestoneId);
    event Withdraw(uint256 amount, uint8 milestoneId);
    
    //wird entfernt
    function setWantsToVote(bool newValue) onlyOwner public{
        wantsToVote = newValue;
    }
    
    event Vote(uint8 milestoneId, votePosition vp);
    
    //wird in Project verschoben
    // erhöht den wahl counter des projects(positiv oder negativ).
    //Problem: wenn man in remix value auf 5 ether stellt und 5 zahlt wird counter um 5 erhöht. Bei wei genau so.
    function vote(uint8 milestoneId, votePosition vp) public {
        uint256 minDonation = project.getMilestoneMinDonToVote(milestoneId);
        if(wantsToVote && (donatedAmountPerMilestone[milestoneId] >= minDonation) && (votedMilestones[milestoneId] == false)){
            if(vp ==votePosition.POSITIVE_VOTE){
                project.setMilestoneVotePositive(milestoneId);
            } else if(vp == votePosition.NEGATIVE_VOTE){
                project.setMilestoneVoteNegative(milestoneId);
            }
            votedMilestones[milestoneId] = true;
            emit Vote(milestoneId,vp);

        }
    }
    
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
    
    //für bestimmten milestone spenden
    //warnen wenn nicht genug geld auf konto?
    //spenden auf nicht existierende milestones möglich
    function deposit(uint256 amount,uint8 milestoneId) onlyOwner payable public {
        require(msg.value == amount);
        donatedAmountPerMilestone[milestoneId] += amount;
        project.setDonatedAmount(milestoneId, amount);
        emit Deposit(amount,milestoneId);
        
    }
    

   //bestimmten betrag von bestimmten Milestone abheben (nur wenn vorher auch so viel gespendet)
    function withdraw(uint256 amount,uint8 milestoneId) onlyOwner payable public {
        require(donatedAmountPerMilestone[milestoneId] >= amount);
        msg.sender.transfer(amount);
        emit Withdraw(amount, milestoneId);
        
    }
    
    //onlyOwner ??
    function getBalanceInMilestone(uint8 milestoneId) view public returns (uint256){
        return donatedAmountPerMilestone[milestoneId];
    }

     
    
}
