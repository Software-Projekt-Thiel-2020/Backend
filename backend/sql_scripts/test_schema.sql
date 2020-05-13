DROP SCHEMA IF EXISTS mydb ;
CREATE SCHEMA IF NOT EXISTS mydb DEFAULT CHARACTER SET utf8 ;
USE mydb ;
CREATE TABLE IF NOT EXISTS mydb.SmartContract (
  idSmartContract INT NOT NULL,
  blockchainAddrSmartContract BINARY(20) NOT NULL,
  PRIMARY KEY (idSmartContract));