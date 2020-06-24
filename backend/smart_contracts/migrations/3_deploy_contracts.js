const Project = artifacts.require("Project");

module.exports = function(deployer) {
  deployer.deploy(Project, 80, web3.utils.fromAscii("TestProject"), 100000, 10);
};
