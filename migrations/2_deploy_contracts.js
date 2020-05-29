const Institution = artifacts.require("Institution");

module.exports = function(deployer) {
  deployer.deploy(Institution);
};
