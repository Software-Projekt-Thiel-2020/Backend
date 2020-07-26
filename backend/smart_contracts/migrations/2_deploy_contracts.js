const Institution = artifacts.require("Institution");

module.exports = function(deployer, network, accounts) {
  deployer.deploy(Institution, accounts[0], accounts[0]);
};
