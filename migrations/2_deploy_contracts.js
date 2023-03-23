var chargeGas = artifacts.require("./chargeGas.sol");

module.exports = function(deployer) {
    var stationPrice = 10000000000000000; // 0.01 eth
    var stationAddress = "0xD4A94BFABd1dc5F751C56AeAcAB43C30AEe72585"; // change this every new ganache startup
    deployer.deploy(chargeGas, stationPrice, stationAddress);
}