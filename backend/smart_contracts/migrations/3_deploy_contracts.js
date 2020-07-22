const Project = artifacts.require("Project");

module.exports = function(deployer, network, accounts) {
  deployer.deploy(Project, accounts[0], accounts[0], 80, web3.utils.fromAscii("TestProject"), 100000, 10);
};
