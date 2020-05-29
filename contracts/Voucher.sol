pragma solidity 0.5.16;

contract Institution{
    
    struct Voucher {
        uint64 expires_unixtime;
        bool used;
        bytes32 description;
    }

    address public institution;
    mapping(address => Voucher[]) voucher;
    
    event newVoucher(address _owner, uint64 _index, bytes32 _description, uint64 expires_unixtime);
    event redeemVoucher(address _owner, uint64 _index, bytes32 _description);
    
    constructor() public{
        institution=msg.sender;
    }
    
    function addVoucher(address _owner,bytes32  _description,uint64 _expires_in_Days) public {
        require(msg.sender==institution);
        Voucher memory v;
        v.expires_unixtime=uint64(now)+(_expires_in_Days*1 days);
        v.description=_description;
        voucher[_owner].push(v);
        uint64 index=uint64(voucher[_owner].length);
        emit newVoucher(_owner, index, v.description, v.expires_unixtime);
    }
    
    function redeem(uint64 _index) public{
        Voucher memory v=voucher[msg.sender][_index];
        require(v.used==false);
        require(v.expires_unixtime>=block.timestamp);
        v.used=true;
        voucher[msg.sender][_index]=v;
        emit redeemVoucher(msg.sender,_index,v.description);
    }
}
