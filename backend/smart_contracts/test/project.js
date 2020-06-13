const Project = artifacts.require("Project");
const truffleAssert = require('truffle-assertions');
const helper = require("../helpers/truffleTestHelper");

const days = (24 * 60 * 60);


contract('Project', (accounts) => {
    let uut;
    let timestamp_now;
    const owner = accounts[0];

    // build up and tear down a new uut contract before each test
    beforeEach(async () => {
        timestamp_now = (await web3.eth.getBlock('latest')).timestamp;
        uut = await Project.new(80, web3.utils.fromAscii("TestProject"), 100000, 10, {from: owner});
    });
    afterEach(async () => {
        // nothing to do
    });


    it('project should be able to be constructed', async () => {
    });

    it('project ctor should revert if partial_payment too big', async () => {
        await truffleAssert.reverts(
            Project.new(101, web3.utils.fromAscii("TestProject"), 100000, 10, {from: owner})
        );
    });

    it('project ctor should revert if partial_payment is 100%', async () => {
        await truffleAssert.reverts(
            Project.new(100, web3.utils.fromAscii("TestProject"), 100000, 10, {from: owner})
        );
    });

    it('project ctor should revert if empty project-name', async () => {
        await truffleAssert.reverts(
            Project.new(80, [], 100000, 10, {from: owner})
        );
    });

    it('project ctor should revert if target amount is 0', async () => {
        await truffleAssert.reverts(
            Project.new(80, [], 0, 10, {from: owner})
        );
    });


    it('project should be able to add single milestone', async () => {
        const test_name = "TestString";
        const test_target_amount = 50000;

        let result = await uut.addMilestone(web3.utils.fromAscii(test_name), test_target_amount, timestamp_now + 2 * days, {from: owner});

        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount, 'event AddMilestone: targetAmount');
            return true;
        });
    });


    it('project should be able to add multiple milestone', async () => {
        const test_name = "TestString";
        const test_name2 = "TestString2";
        const test_target_amount = 50000;
        const test_target_amount2 = 75000;

        let result = await uut.addMilestone(web3.utils.fromAscii(test_name), test_target_amount, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount, 'event AddMilestone: targetAmount');
            return true;
        });

        await helper.advanceTimeAndBlock(1);

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
    });
});
