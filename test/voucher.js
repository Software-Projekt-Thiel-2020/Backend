const Institution = artifacts.require("Institution");

contract('MetaCoin', (accounts) => {
  it('should be deployable', async () => {
    const uut = await Institution.deployed();
  });

});
