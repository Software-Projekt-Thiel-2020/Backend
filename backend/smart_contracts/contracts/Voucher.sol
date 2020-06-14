pragma solidity ^0.5.16;
/// @title SmartContract zum Verwalten von Gutscheinen
contract Institution {

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
        institution = msg.sender;
    }

    /// @notice fuegt neuen Gutschein hinzu
    /// @notice das Ablaufdatum wird in Tagen angegeben, Schalttage sind selber zu berechnen
    /// @param _owner ethereum address des Gutschein Besitzers
    /// @param _description Beschreibung des Gutscheins in hex
    /// @param _expires_in_Days Zeit in Tagen bis der Gutschein ablaeuft
    function addVoucher(address _owner, bytes32 _description, uint64 _expires_in_Days) public {
        require(msg.sender == institution);
        Voucher memory v;

        v.expires_unixtime = uint64(now) + (_expires_in_Days * 1 days);
        v.description = _description;
        uint64 index = uint64(voucher[_owner].length);
        voucher[_owner].push(v);

        emit newVoucher(_owner, index, v.description, v.expires_unixtime);
    }

    /// @notice Funktion zum einloesen des Gutscheins
    /// @notice nur der Besitzer des Gutscheins kann diesen einloesen
    /// @param _index index des Gutscheins der eingeloest werden soll
    function redeem(uint64 _index) public {
        require(voucher[msg.sender].length > _index);
        Voucher memory v = voucher[msg.sender][_index];
        require(v.used == false);
        require(v.expires_unixtime >= block.timestamp);

        voucher[msg.sender][_index].used = true;

        emit redeemVoucher(msg.sender, _index, v.description);
    }
}
