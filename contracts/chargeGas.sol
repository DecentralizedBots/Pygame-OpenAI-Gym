// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract chargeGas {
  // charge price per 1/100
    uint chargePrice;

    // gas station address, who gets the money
    address payable public gasAddress;

    // error handling
    error fullTank();
    error highGasLevel(uint gasLevel);
    error lowBalance();
    error notSent();

    constructor(uint chargePrice_, address payable gasAddress_) {
        chargePrice = chargePrice_;
        gasAddress = gasAddress_;
    }

    function charge(address payable msgSender) public payable{
        (bool sent, bytes memory data) = msgSender.call{value: chargePrice}("");
        require(sent, "Failed to send Ether");
    }
}

//    function charge(uint gasLevel) external payable {
//        if (gasLevel > 100) {
//            revert highGasLevel(gasLevel);
//        }
//
//        if (gasLevel == 100) {
//            revert fullTank();
//        }
//
//        uint difference = 100 - gasLevel;
//        uint totalChargePrice = difference * chargePrice;
//
//        if (msg.sender.balance < totalChargePrice) {
//            revert lowBalance();
//        }
//
//        gasAddress.transfer(totalChargePrice);
//        payable(msg.sender).transfer(totalChargePrice);
//    }
