const Institution = artifacts.require("Institution");
const truffleAssert = require('truffle-assertions');
const helper = require("../helpers/truffleTestHelper");

const days = (24 * 60 * 60);


contract('Institution', (accounts) => {
    return;
    let uut;
    const owner = accounts[0];
    const test_description = "TestString";

    // build up and tear down a new uut contract before each test
    beforeEach(async () => {
        uut = await Institution.new({from: owner});
    });
    afterEach(async () => {
        // nothing to do
    });

    it('institution should be able to be constructed', async () => {
    });

    it('institution should be able to create a voucher', async () => {
        const receiver = accounts[1];
        const expires_days = 1;
        const expires = Math.floor(new Date().getTime() / 1000) + expires_days * days;

        let result = await uut.addVoucher(receiver, web3.utils.fromAscii(test_description), expires_days, {from: owner});

        truffleAssert.eventEmitted(result, 'newVoucher', (ev) => {
            assert.equal(ev._owner, receiver, 'event newVoucher: owner');
            assert.equal(ev._index, 0, 'event newVoucher: index');
            assert.equal(web3.utils.toAscii(ev._description).replace(/\0/g, ''), test_description, 'event newVoucher: description');

            assert.isAtLeast(Math.floor(ev.expires_unixtime), expires - 5, 'event newVoucher: expires');
            assert.isAtMost(Math.floor(ev.expires_unixtime), expires + 5, 'event newVoucher: expires'); // for VERY slow machines 5 seconds
            return true;
        });
    });
    it('someone else shouldnt be able to add a voucher', async () => {
        await truffleAssert.reverts(
            uut.addVoucher(accounts[2], web3.utils.fromAscii(test_description), 0, {from: accounts[1]})
        );
    });

    it('receiver can redeem voucher', async () => {
        const receiver = accounts[1];
        const expires_days = 1;
        const voucher_index = 0;

        await uut.addVoucher(receiver, web3.utils.fromAscii(test_description), expires_days, {from: owner});

        let result = await uut.redeem(voucher_index, {from: receiver});

        truffleAssert.eventEmitted(result, 'redeemVoucher', (ev) => {
            assert.equal(ev._owner, receiver, 'event redeemVoucher: owner');
            assert.equal(ev._index, voucher_index, 'event redeemVoucher: index');
            assert.equal(web3.utils.toAscii(ev._description).replace(/\0/g, ''), test_description, 'event redeemVoucher: description');
            return true;
        });
    });

    it('cant redeem already used voucher', async () => {
        const receiver = accounts[1];
        const voucher_index = 0;

        let result = await uut.addVoucher(receiver, web3.utils.fromAscii(test_description), 0, {from: owner});
        truffleAssert.eventEmitted(result, 'newVoucher', (ev) => {
            assert.equal(true, true, 'newVoucher ok');
            return true;
        });
        result = await uut.redeem(voucher_index, {from: receiver});
        truffleAssert.eventEmitted(result, 'redeemVoucher', (ev) => {
            assert.equal(true, true, 'first redeem voucher ok');
            return true;
        });

        await truffleAssert.reverts(
            uut.redeem(voucher_index, {from: receiver})
        );
    });

    it('cant redeem expired voucher', async () => {
        const receiver = accounts[1];
        const expires_days = 10;
        const voucher_index = 0;

        await uut.addVoucher(receiver, web3.utils.fromAscii(test_description), expires_days, {from: owner});

        await helper.advanceTimeAndBlock(1 + expires_days * days); // wait for voucher to expire

        await truffleAssert.reverts(
            uut.redeem(voucher_index, {from: receiver})
        );
    });

    it('cant redeem voucher if you have none', async () => {
        const receiver = accounts[1];
        const voucher_index = 0;

        await truffleAssert.reverts(
            uut.redeem(voucher_index, {from: receiver})
        );
    });

    it('cant redeem non-existant voucher', async () => {
        const receiver = accounts[1];
        await uut.addVoucher(receiver, web3.utils.fromAscii(test_description), 0, {from: owner});

        await truffleAssert.reverts(
            uut.redeem(123, {from: receiver})
        );
    });
});
