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

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
    });

    it('project shouldnt be able to add smaller milestone', async () => {
        const test_name = "TestString";
        const test_name2 = "TestString2";
        const test_target_amount = 50000;
        const test_target_amount2 = 5000;

        let result = await uut.addMilestone(web3.utils.fromAscii(test_name), test_target_amount, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount, 'event AddMilestone: targetAmount');
            return true;
        });

        await helper.advanceTimeAndBlock(1);

        await truffleAssert.reverts(
            uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner})
        );
    });

    it('project should be able to donate-lite', async () => {
        const test_amount = 1000;

        let result = await uut.donate_lite({from: accounts[1], value: test_amount});

        truffleAssert.eventEmitted(result, 'Donate_Light', (ev) => {
            assert.equal(ev.amount, test_amount, 'event AddMilestone: targetAmount');
            return true;
        });
    });

    it('project should be able to donate-lite 2', async () => {
        const test_amount = 1234567890;

        let result = await uut.donate_lite({from: accounts[1], value: test_amount});

        truffleAssert.eventEmitted(result, 'Donate_Light', (ev) => {
            assert.equal(ev.amount, test_amount, 'event AddMilestone: targetAmount');
            return true;
        });
    });


    it('project should be able to register as donator', async () => {
        await uut.register({from: accounts[1]});
    });

    it('project should be able to donate without vote (no milestones)', async () => {
        const test_amount = 1234567890;

        await uut.register({from: accounts[1]});
        let result = await uut.donate(false, {from: accounts[1], value: test_amount});

        truffleAssert.eventEmitted(result, 'Donate', (ev) => {
            assert.equal(ev.amount, test_amount, 'event Donate: amount');
            assert.equal(ev.milestoneId, 0, 'event Donate: activeMilestone');
            assert.equal(ev.donor_add, accounts[1], 'event Donate: sender');
            assert.equal(ev.wantsToVote, false, 'event Donate: _wantsToVote');
            return true;
        });
    });

    it('project should be able to donate with vote (with milestones)', async () => {
        const test_name = "TestString";
        const test_name2 = "TestString2";
        const test_target_amount = 50000;
        const test_target_amount2 = 75000;
        const test_amount = 1000;

        let result = await uut.addMilestone(web3.utils.fromAscii(test_name), test_target_amount, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount, 'event AddMilestone: targetAmount');
            return true;
        });

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
        /////////////////////////////////////////

        await uut.register({from: accounts[1]});
        result = await uut.donate(true, {from: accounts[1], value: test_amount});

        truffleAssert.eventEmitted(result, 'Donate', (ev) => {
            assert.equal(ev.amount, test_amount, 'event Donate: amount');
            assert.equal(ev.milestoneId, 0, 'event Donate: activeMilestone');
            assert.equal(ev.donor_add, accounts[1], 'event Donate: sender');
            assert.equal(ev.wantsToVote, true, 'event Donate: _wantsToVote');
            return true;
        });
    });


    it('project should be able to payingOutActiveMilestoneAll', async () => {
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

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
        /////////////////////////////////////////

        await uut.register({from: accounts[1]});
        await uut.donate(false, {from: accounts[1], value: test_target_amount});

        result = await uut.payingOutActiveMilestoneAll(0, {from: owner});

        truffleAssert.eventEmitted(result, 'PayingOutAll', (ev) => {
            assert.equal(ev.amount, test_target_amount, 'event PayingOutAll: amount');
            assert.equal(ev.milestoneId, 0, 'event PayingOutAll: milestoneId');
            return true;
        });
    });


    /* it('project should be able to vote', async () => {
     const test_name = "TestString";
     const test_target_amount = 50000;
 const test_name2 = "TestString2";
 const test_target_amount2 = 75000;

     let result = await uut.addMilestone(web3.utils.fromAscii(test_name), test_target_amount, timestamp_now + 2 * days, {from: owner});
     truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
         assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name, 'event AddMilestone: name');
         assert.equal(ev._amount, test_target_amount, 'event AddMilestone: targetAmount');
         return true;
     });

     result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
     truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
         assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
         assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
         return true;
     });

     /////////////////////////////////////////

     await uut.register({from: accounts[1]});
     await uut.donate(true, {from: accounts[1], value: test_target_amount});


     result = await uut.vote(0,0, {from: accounts[1]});

     truffleAssert.eventEmitted(result, 'Vote', (ev) => {
         assert.equal(ev.milestoneId, 0, 'event Vote: milestoneId');
     //assert.equal(ev.votePosition,0,'event Vote: votePosition'); //enums können
         return true;
     });

 //funktioniert nicht ??
 //let temp = uut.milestones.call(0);
 //let milestoneVote = temp[3];
 //assert.equal(milestoneVote,1);
 //milestoneVote = temp[4];
 //assert.equal(milestoneVote,0);

 });*/


    it('project should be able to payingOutActiveMilestonePart if more positive votes', async () => {
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

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
        ////////////////////////////////////////

        await uut.register({from: accounts[1]});
        await uut.donate(true, {from: accounts[1], value: test_target_amount});
        await uut.vote(0, 0, {from: accounts[1]});

        await helper.advanceTimeAndBlock(4 * days);

        result = await uut.payingOutActiveMilestonePart(0, {from: owner});

        let expected = (test_target_amount / 100) * 80;

        truffleAssert.eventEmitted(result, 'PayingOutPart', (ev) => {
            assert.equal(ev.amount, expected, 'event PayingOutPart: amount');
            assert.equal(ev.milestoneId, 0, 'event PayingOutPart: milestoneId');
            return true;
        });

        expected = await uut.milestones.call(0);
        assert.equal(expected[5], true);

    });


    it('project only owner is able to create milestones', async () => {
        const test_name = "TestString";
        const test_target_amount = 50000;

        await truffleAssert.reverts(
            uut.addMilestone(web3.utils.fromAscii(test_name), test_target_amount, timestamp_now + 2 * days, {from: accounts[1]})
        );

    });

    it('project only owner should be able to payingOutActiveMilestonePart', async () => {
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

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
        ////////////////////////////////////////


        await uut.register({from: accounts[1]});
        await uut.donate(true, {from: accounts[1], value: test_target_amount});
        await uut.vote(0, 0, {from: accounts[1]});

        await helper.advanceTimeAndBlock(4 * days);

        await truffleAssert.reverts(
            uut.payingOutActiveMilestonePart(0, {from: accounts[1]})
        );


    });

    it('project only owner should be able to payingOutActiveMilestoneAll', async () => {
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

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
        /////////////////////////////////////////

        await uut.register({from: accounts[1]});
        await uut.donate(false, {from: accounts[1], value: test_target_amount});

        await truffleAssert.reverts(
            uut.payingOutActiveMilestoneAll(0, {from: accounts[1]})
        );

    });

    it('project should be able to payingOutProject without partialPayment before', async () => {
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

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
        /////////////////////////////////////////

        await uut.register({from: accounts[1]});
        await uut.donate(false, {from: accounts[1], value: 100000});

        result = await uut.payingOutProject({from: owner});


        truffleAssert.eventEmitted(result, 'PayingOutProject', (ev) => {
            assert.equal(ev._amount, 100000, 'event PayingOutProject: amount');
            return true;
        });


    });

    it('project should be able to payingOutProject with partialPayment before', async () => {
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

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
        /////////////////////////////////////////

        await uut.register({from: accounts[1]});
        await uut.donate(true, {from: accounts[1], value: 100000});
        await uut.vote(0, 0, {from: accounts[1]});

        await helper.advanceTimeAndBlock(4 * days);

        result = await uut.payingOutActiveMilestonePart(0, {from: owner});

        let expected = (test_target_amount / 100) * 80;
        let rest = 100000 - expected;

        truffleAssert.eventEmitted(result, 'PayingOutPart', (ev) => {
            assert.equal(ev.amount, expected, 'event PayingOutPart: amount');
            assert.equal(ev.milestoneId, 0, 'event PayingOutPart: milestoneId');
            return true;
        });

        result = await uut.payingOutProject({from: owner});
        truffleAssert.eventEmitted(result, 'PayingOutProject', (ev) => {
            assert.equal(ev._amount, rest, 'event PayingOutProject: amount');
            return true;
        });
    });

    it('project should not be able to payingOutProject two times', async () => {
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

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
        /////////////////////////////////////////

        await uut.register({from: accounts[1]});
        await uut.donate(true, {from: accounts[1], value: 100000});
        await uut.vote(0, 0, {from: accounts[1]});

        result = await uut.payingOutProject({from: owner});
        truffleAssert.eventEmitted(result, 'PayingOutProject', (ev) => {
            assert.equal(ev._amount, 100000, 'event PayingOutProject: amount');
            return true;
        });

        result = await uut.payingOutProject({from: owner});
        truffleAssert.eventEmitted(result, 'PayingOutProject', (ev) => {
            assert.equal(ev._amount, 0, 'event PayingOutProject: amount');
            return true;
        });


    });

    it('project only owner should be able to payingOutProject', async () => {
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

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
        /////////////////////////////////////////

        await uut.register({from: accounts[1]});
        await uut.donate(false, {from: accounts[1], value: 100000});

        await truffleAssert.reverts(
            uut.payingOutProject({from: accounts[1]})
        );

    });

    it('project should be able to retract', async () => {
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

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
        ////////////////////////////////////////

        await uut.register({from: accounts[1]});
        await uut.donate(true, {from: accounts[1], value: 10000});

        result = await uut.retract({from: accounts[1]});


        truffleAssert.eventEmitted(result, 'Retract', (ev) => {
            assert.equal(ev.amount, 10000, 'event Retract: amount');
            assert.equal(ev.milestoneId, 0, 'event Retract: milestoneId');
            assert.equal(ev.donor, accounts[1], 'event Retract: donor');
            return true;
        });


    });

    it('project onwer should not be able to register', async () => {

        await truffleAssert.reverts(
            uut.register({from: accounts[0]})
        );
        
    });

    it('project should not be able to payingOutActiveMilestonePart if more negative votes', async () => {
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

        result = await uut.addMilestone(web3.utils.fromAscii(test_name2), test_target_amount2, timestamp_now + 2 * days, {from: owner});
        truffleAssert.eventEmitted(result, 'AddMilestone', (ev) => {
            assert.equal(web3.utils.toAscii(ev._name).replace(/\0/g, ''), test_name2, 'event AddMilestone: name');
            assert.equal(ev._amount, test_target_amount2, 'event AddMilestone: targetAmount');
            return true;
        });
        ////////////////////////////////////////

        await uut.register({from: accounts[1]});
        await uut.donate(true, {from: accounts[1], value: test_target_amount});
        await uut.vote(0, 1, {from: accounts[1]});

        await helper.advanceTimeAndBlock(4 * days);

        await truffleAssert.reverts(
            uut.payingOutActiveMilestonePart(0, {from: owner})
        );

    });




});