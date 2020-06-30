const Project = artifacts.require("Project");

module.exports = function(deployer) {
  deployer.deploy(Project, '0x53e5013cf3B4CC2ebEa3AC676661A30D073D2916', 80, web3.utils.fromAscii("TestProject"), 100000, 10);
};
