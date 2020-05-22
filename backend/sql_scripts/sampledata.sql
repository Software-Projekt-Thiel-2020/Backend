insert into SmartContract values(1, '666');
insert into SmartContract values(2, '1337');

insert into User values(1, 'LoetkolbenLudwig', 'Ludwig', 'Loetkolben', 'll@swp.de', '4242424242', '2424242424');
insert into User values(2, 'MSDOSManfred', 'Manfred', 'MSDOS', 'msdosm@swp.de', '133713371337', '733173317331');
insert into User values(3, 'HardwareHansPeter', 'HansPeter', 'Hardware', 'hwhp@swp.de', '6668866688', '8866688666');
insert into User values(4, 'BIOSBernhard', 'Bernhard', 'BIOS', 'biosb@swp.de', '1003310033', '3300133001');
insert into User values(5, 'OdinsonThor', 'Thor', 'Odinson', 'ot@swp.de', '268110268110', '011862011862');

insert into Institution values(1, 'MSGraphic', 'www.msgraphic.com', 1);
insert into Institution values(2, 'SWP', 'www.swp.com', 1);
insert into Institution values(3, 'Asgard Inc.', 'www.asgard.as', 1);
insert into Institution values(4, 'Blackhole', '127.0.0.1', 1);

insert into Project values(1, 'Computer malt Bild', 'www.cmb.de', 2, 1);
insert into Project values(2, 'Rangaroek verteidigen', 'www.asgard.as', 2, 3);
insert into Project values(3, 'Softwareprojekt 2020', 'www.swp.de', 2, 3);

insert into Milestone values(1, 1000, 112, 0, 600000, 1);
insert into Milestone values(2, 2000, 112, 0, 1200000, 1);
insert into Milestone values(3, 3000, 112, 0, 2400000, 1);
insert into Milestone values(4, 1000, 88, 0, 121212121, 2);
insert into Milestone values(5, 2000, 88, 0, 321123448, 2);
insert into Milestone values(6, 3000, 88, 0, 654654832, 3);
insert into Milestone values(7, 5000, 666, 0, 100000000, 1);

insert into Voucher values(1, 'Von Computer gemaltes Bild', 'Der Computer malt ein täuschend echtes Bild für sie!', 0, 600000000, 1);
insert into Voucher values(2, 'Software', 'Software für ein Hochschulprojet', 0, 600000000, 1);

insert into VoucherUser values(1, 1);
insert into VoucherUser values(2, 1);
insert into VoucherUser values(3, 1);
insert into VoucherUser values(4, 1);

insert into Transaction(idTransaction, fkSmartContractTransaction, fkUserTransaction) values(1, 1, 1);
insert into Transaction(idTransaction, fkSmartContractTransaction, fkUserTransaction) values(2, 1, 2);
insert into Transaction(idTransaction, fkSmartContractTransaction, fkUserTransaction) values(3, 1, 3);
insert into Transaction(idTransaction, fkSmartContractTransaction, fkUserTransaction) values(4, 1, 4);

insert into Donation values(1, 100, 1, 1);
insert into Donation values(2, 100, 2, 2);
insert into Donation values(3, 100, 3, 3);
insert into Donation values(4, 100, 4, 4);
