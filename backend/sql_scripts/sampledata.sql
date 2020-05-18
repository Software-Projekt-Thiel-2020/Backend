insert into smartcontract values(1, '666');
insert into smartcontract values(2, '1337');

insert into user values(1, 'LoetkolbenLudwig', 'Ludwig', 'Loetkolben', 'll@swp.de', '4242424242', '2424242424');
insert into user values(2, 'MSDOSManfred', 'Manfred', 'MSDOS', 'msdosm@swp.de', '133713371337', '733173317331');
insert into user values(3, 'HardwareHansPeter', 'HansPeter', 'Hardware', 'hwhp@swp.de', '6668866688', '8866688666');
insert into user values(4, 'BIOSBernhard', 'Bernhard', 'BIOS', 'biosb@swp.de', '1003310033', '3300133001');
insert into user values(5, 'OdinsonThor', 'Thor', 'Odinson', 'ot@swp.de', '268110268110', '011862011862');

insert into institution values(1, 'MSGraphic', 'www.msgraphic.com', 1);
insert into institution values(2, 'SWP', 'www.swp.com', 1);
insert into institution values(3, 'Asgard Inc.', 'www.asgard.as', 1);
insert into institution values(4, 'Blackhole', '127.0.0.1', 1);

insert into project values(1, 'Computer malt Bild', 'www.cmb.de', 2, 1);
insert into project values(2, 'Rangaroek verteidigen', 'www.asgard.as', 2, 3);
insert into project values(3, 'Softwareprojekt 2020', 'www.swp.de', 2, 3);

insert into milestone values(1, 1000, 112, 0, 600000, 1); 
insert into milestone values(2, 2000, 112, 0, 1200000, 1); 
insert into milestone values(3, 3000, 112, 0, 2400000, 1); 
insert into milestone values(4, 1000, 88, 0, 121212121, 2); 
insert into milestone values(5, 2000, 88, 0, 321123448, 2); 
insert into milestone values(6, 3000, 88, 0, 654654832, 3); 
insert into milestone values(7, 5000, 666, 0, 100000000, 1); 

insert into voucher values(1, 'Von Computer gemaltes Bild', 'Der Computer malt ein täuschend echtes Bild für sie!', 0, 600000000, 1);
insert into voucher values(2, 'Software', 'Software für ein Hochschulprojet', 0, 600000000, 1);

insert into voucheruser values(1, 1);
insert into voucheruser values(2, 1);
insert into voucheruser values(3, 1);
insert into voucheruser values(4, 1);

insert into transaction(idTransaction, fkSmartContractTransaction, fkUserTransaction) values(1, 1, 1);
insert into transaction(idTransaction, fkSmartContractTransaction, fkUserTransaction) values(2, 1, 2);
insert into transaction(idTransaction, fkSmartContractTransaction, fkUserTransaction) values(3, 1, 3);
insert into transaction(idTransaction, fkSmartContractTransaction, fkUserTransaction) values(4, 1, 4);

insert into donation values(1, 100, 1, 1);
insert into donation values(2, 100, 2, 2);
insert into donation values(3, 100, 3, 3);
insert into donation values(4, 100, 4, 4);

