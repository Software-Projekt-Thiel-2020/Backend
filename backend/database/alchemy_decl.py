from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, BINARY, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'Project'
    idProject = Column(Integer, primary_key=True)
    nameProject = Column(VARCHAR(45))
    webpageProject = Column(VARCHAR(256))
    fkSmartContractProject = Column(Integer, ForeignKey('SmartContract.idSmartContract'))
    fkInstitutionProject = Column(Integer, ForeignKey('Institution.idInstitution'))


class SmartContract(Base):
    __tablename__ = 'SmartContract'
    idSmartContract = Column(Integer, primary_key=True)
    blockchainAddrSmartContract = Column(BINARY(20))


class Milestone(Base):
    __tablename__ = 'Milestone'
    idMilestone = Column(Integer, primary_key=True)
    goalMilestone = Column(Integer)
    requiredVotesMilestone = Column(Integer)
    currentVotesMilestone = Column(Integer)
    untilBlockMilestone = Column(Integer)
    fkProjectMilestone = Column(Integer, ForeignKey('Project.idProject'))


class Institution(Base):
    __tablename__ = 'Institution'
    idInstitution = Column(Integer, primary_key=True)
    nameInstitution = Column(VARCHAR(45))
    webpageInstitution = Column(VARCHAR(256))
    fkSmartContractInstitution = Column(Integer, ForeignKey('SmartContract.idSmartContract'))


class Voucher(Base):
    __tablename__ = 'Voucher'
    idVoucher = Column(Integer, primary_key=True)
    titleVoucher = Column(VARCHAR(32))
    descriptionVoucher = Column(VARCHAR(1024))
    usedVoucher = Column(Integer())
    untilBlockVoucher = Column(Integer)
    fkInstitutionVoucher = Column(Integer, ForeignKey('Institution.idInstitution'))


class User(Base):
    __tablename__ = 'User'
    idUser = Column(Integer, primary_key=True)
    usernameUser = Column(VARCHAR(45))
    firstnameUser = Column(VARCHAR(45))
    lastnameUser = Column(VARCHAR(45))
    emailUser = Column(VARCHAR(45))
    publickeyUser = Column(BINARY(64))
    privatekeyUser = Column(BINARY(128))


class Donation(Base):
    __tablename__ = 'Donation'
    idDonation = Column(Integer, primary_key=True)
    amountDonation = Column(Integer)
    fkMilestoneDonation = Column(Integer, ForeignKey('Milestone.idMilestone'))
    fkUserDonation = Column(Integer, ForeignKey('User.idUser'))


class Transaction(Base):
    __tablename__ = 'Transaction'
    idTransaction = Column(Integer, primary_key=True)
    dateTransaction = Column(TIMESTAMP)
    fkSmartContractTransaction = Column(Integer, ForeignKey('SmartContract.idSmartContract'))
    fkUserTransaction = Column(Integer, ForeignKey('User.idUser'))


class VoucherUser(Base):
    __tablename__ = 'VoucherUser'
    fkUserVoucherUser = Column(Integer, ForeignKey('User.idUser'), primary_key=True)
    fkVucherVoucherUser = Column(Integer, ForeignKey('Voucher.idVoucher'), primary_key=True)
