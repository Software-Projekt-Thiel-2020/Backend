"""Defines the (declarative_base) model."""
from datetime import datetime
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, BINARY, TIMESTAMP, Table, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import relationship

BASE: DeclarativeMeta = declarative_base()


class Project(BASE):
    __tablename__ = 'Project'
    idProject = Column(Integer, primary_key=True)
    nameProject = Column(VARCHAR(256))
    webpageProject = Column(VARCHAR(256))

    smartcontract_id = Column(Integer, ForeignKey('SmartContract.idSmartContract'))
    smartcontract = relationship("SmartContract", back_populates="projects")

    institution_id = Column(Integer, ForeignKey('Institution.idInstitution'))
    institution = relationship("Institution", back_populates="projects")

    milestones = relationship("Milestone", back_populates="project")


class SmartContract(BASE):
    __tablename__ = 'SmartContract'
    idSmartContract = Column(Integer, primary_key=True)
    blockchainAddrSmartContract = Column(BINARY(20))

    projects = relationship("Project", back_populates="smartcontract")
    institutions = relationship("Institution", back_populates="smartcontract")
    transactions = relationship("Transaction", back_populates="smartcontract")


class Milestone(BASE):
    __tablename__ = 'Milestone'
    idMilestone = Column(Integer, primary_key=True)
    goalMilestone = Column(Integer)
    requiredVotesMilestone = Column(Integer)
    currentVotesMilestone = Column(Integer)
    untilBlockMilestone = Column(Integer)

    project_id = Column(Integer, ForeignKey('Project.idProject'))
    project = relationship("Project", back_populates="milestones")

    donations = relationship("Donation", back_populates="")


class Institution(BASE):
    __tablename__ = 'Institution'
    idInstitution = Column(Integer, primary_key=True)
    nameInstitution = Column(VARCHAR(256))
    webpageInstitution = Column(VARCHAR(256))

    projects = relationship("Project", back_populates="institution")

    smartcontract_id = Column(Integer, ForeignKey('SmartContract.idSmartContract'))
    smartcontract = relationship("SmartContract", back_populates="institutions")

    vouchers = relationship("Voucher", back_populates="institution")


VOUCHER_USER_TABLE = Table("VoucherUser", BASE.metadata,
                           Column("idUser", Integer, ForeignKey("User.idUser"), primary_key=True),
                           Column("idVoucher", Integer, ForeignKey("Voucher.idVoucher"), primary_key=True)
                           )


class Voucher(BASE):
    __tablename__ = 'Voucher'
    idVoucher = Column(Integer, primary_key=True)
    titleVoucher = Column(VARCHAR(32))
    descriptionVoucher = Column(VARCHAR(1024))
    usedVoucher = Column(BOOLEAN)
    untilBlockVoucher = Column(Integer)

    institution_id = Column(Integer, ForeignKey('Institution.idInstitution'))
    institution = relationship("Institution", back_populates="vouchers")

    users = relationship("User", secondary=VOUCHER_USER_TABLE, back_populates="vouchers")


class User(BASE):
    __tablename__ = 'User'
    idUser = Column(Integer, primary_key=True)
    usernameUser = Column(VARCHAR(45))
    firstnameUser = Column(VARCHAR(45))
    lastnameUser = Column(VARCHAR(45))
    emailUser = Column(VARCHAR(45))
    publickeyUser = Column(BINARY(64))
    privatekeyUser = Column(BINARY(128))
    authToken = Column(VARCHAR(2048))

    donations = relationship("Donation", back_populates="user")

    transactions = relationship("Transaction", back_populates="user")

    vouchers = relationship("Voucher", secondary=VOUCHER_USER_TABLE, back_populates="users")


class Donation(BASE):
    __tablename__ = 'Donation'
    idDonation = Column(Integer, primary_key=True)
    amountDonation = Column(Integer)

    user_id = Column(Integer, ForeignKey('User.idUser'))
    user = relationship("User", back_populates="donations")

    milestone_id = Column(Integer, ForeignKey('Milestone.idMilestone'))
    milestone = relationship("Milestone", back_populates="donations")


class Transaction(BASE):
    __tablename__ = 'Transaction'
    idTransaction = Column(Integer, primary_key=True)
    dateTransaction = Column(TIMESTAMP)

    smartcontract_id = Column(Integer, ForeignKey('SmartContract.idSmartContract'))
    smartcontract = relationship("SmartContract", back_populates="transactions")

    user_id = Column(Integer, ForeignKey('User.idUser'))
    user = relationship("User", back_populates="transactions")


# sw2020testuser1.id.blockstack - shortened
TOKEN_1 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyNGE1OTFkNS1lOGJiLTQwMzYtYWE0Ni1hNzg5MjU2ZDVjZDYiLCJpYX" \
          "QiOjE1OTEyMjUyMzIsImV4cCI6MTU5MzgxNzIzMiwiaXNzIjoiZGlkOmJ0Yy1hZGRyOjE0Z1N4eFhZdzlXbTNoYWoxaGVKYXQ1ZGdpe" \
          "HF0YVJ3a3MiLCJwdWJsaWNfa2V5cyI6WyIwMzliZWM4NjkxMGViZmVmMGU4ZmE3YmE2OTQ1MWU1ZjljNDU1NjhmZDFhMmY4MDQ5MzM2" \
          "MWFlMzUzOGM2N2Y3YmIiXSwidXNlcm5hbWUiOiJzdzIwMjB0ZXN0dXNlcjEuaWQuYmxvY2tzdGFjayIsImNvcmVfdG9rZW4iOm51bGw" \
          "sImVtYWlsIjpudWxsLCJwcm9maWxlX3VybCI6Imh0dHBzOi8vZ2FpYS5ibG9ja3N0YWNrLm9yZy9odWIvMTRnU3h4WFl3OVdtM2hhaj" \
          "FoZUphdDVkZ2l4cXRhUndrcy9wcm9maWxlLmpzb24iLCJodWJVcmwiOiJodHRwczovL2h1Yi5ibG9ja3N0YWNrLm9yZyIsImJsb2Nrc" \
          "3RhY2tBUElVcmwiOiJodHRwczovL2NvcmUuYmxvY2tzdGFjay5vcmciLCJ2ZXJzaW9uIjoiMS4zLjEifQ.5Nhd7TWhXhwkkkNOZCHUc" \
          "MSX4ykE6Fdm5-N7yxA60ZI"

# sw2020testuser2.id.blockstack
TOKEN_2 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxZjJiYzcyNy03Y2ZhLTQ5NDEtOTk4ZC03YjIyMGEwOTg2NmYiLCJpYXQi" \
          "OjE1OTEyMjU0OTYsImV4cCI6MTU5MzgxNzQ5NiwiaXNzIjoiZGlkOmJ0Yy1hZGRyOjFIMlQxY0Rmd3lZZFlra1pFUkhmQUh4SkJxaDNie" \
          "TlWd2kiLCJwdWJsaWNfa2V5cyI6WyIwMzgzNGE2MTI3NTc0NzhiMjlhMGU0ZjAxNTdiMjcwYTk3OTUzNzc1MTVhNjJkMGE2M2EyNWQ1Nj" \
          "BmMDgxOGU5NWIiXSwidXNlcm5hbWUiOiJzdzIwMjB0ZXN0dXNlcjIuaWQuYmxvY2tzdGFjayIsImNvcmVfdG9rZW4iOm51bGwsImVtYWl" \
          "sIjpudWxsLCJwcm9maWxlX3VybCI6Imh0dHBzOi8vZ2FpYS5ibG9ja3N0YWNrLm9yZy9odWIvMUgyVDFjRGZ3eVlkWWtrWkVSSGZBSHhK" \
          "QnFoM2J5OVZ3aS9wcm9maWxlLmpzb24iLCJodWJVcmwiOiJodHRwczovL2h1Yi5ibG9ja3N0YWNrLm9yZyIsImJsb2Nrc3RhY2tBUElVc" \
          "mwiOiJodHRwczovL2NvcmUuYmxvY2tzdGFjay5vcmciLCJ2ZXJzaW9uIjoiMS4zLjEifQ.GLsCrvh3jxopSwHTQeFA57AQ-eeL_ZbXto8" \
          "RtzioxMw"


def add_sample_data(db_session):  # pylint:disable=too-many-statements
    """
    Adds some sample data.

    :param db_session: DB_SESSION object
    :return: -
    """
    session = db_session()

    smartcontracts: List[SmartContract] = [
        SmartContract(idSmartContract=1,
                      blockchainAddrSmartContract=bytes("666", encoding="utf-8")),
        SmartContract(idSmartContract=2,
                      blockchainAddrSmartContract=bytes("1337", encoding="utf-8")),
    ]

    users: List[User] = [
        User(idUser=1,
             usernameUser="LoetkolbenLudwig",
             firstnameUser="Ludwig", lastnameUser="Loetkolben",
             emailUser="ll@swp.de",
             publickeyUser=bytes("4242424242", encoding="utf-8"),
             privatekeyUser=bytes("2424242424", encoding="utf-8")),
        User(idUser=2,
             usernameUser="MSDOSManfred",
             firstnameUser="Manfred", lastnameUser="MSDOS",
             emailUser="msdosm@swp.de",
             publickeyUser=bytes("133713371337", encoding="utf-8"),
             privatekeyUser=bytes("733173317331", encoding="utf-8")),
        User(idUser=3,
             usernameUser="HardwareHansPeter",
             firstnameUser="HansPeter", lastnameUser="Hardware",
             emailUser="hwhp@swp.de",
             publickeyUser=bytes("6668866688", encoding="utf-8"),
             privatekeyUser=bytes("8866688666", encoding="utf-8")),
        User(idUser=4,
             usernameUser="BIOSBernhard",
             firstnameUser="Bernhard", lastnameUser="BIOS",
             emailUser="biosb@swp.de",
             publickeyUser=bytes("1003310033", encoding="utf-8"),
             privatekeyUser=bytes("3300133001", encoding="utf-8")),
        User(idUser=5,
             usernameUser="OdinsonThor",
             firstnameUser="Thor", lastnameUser="Odinson",
             emailUser="ot@swp.de",
             publickeyUser=bytes("268110268110", encoding="utf-8"),
             privatekeyUser=bytes("011862011862", encoding="utf-8")),
        User(idUser=6,
             usernameUser="sw2020testuser1.id.blockstack",
             firstnameUser="testuser1", lastnameUser="sw2020",
             emailUser="testuser1@example.com",
             publickeyUser=bytes("14234132", encoding="utf-8"),
             privatekeyUser=bytes("2344322134", encoding="utf-8"),
             authToken=TOKEN_1),
        User(idUser=7,
             usernameUser="sw2020testuser2.id.blockstack",
             firstnameUser="testuser2", lastnameUser="sw2020",
             emailUser="testuser2@example.com",
             publickeyUser=bytes("14234132", encoding="utf-8"),
             privatekeyUser=bytes("2344322134", encoding="utf-8"),
             authToken=TOKEN_2),
    ]

    institutions: List[Institution] = [
        Institution(idInstitution=1,
                    nameInstitution="MSGraphic",
                    webpageInstitution="www.msgraphic.com"),
        Institution(idInstitution=2,
                    nameInstitution="SWP",
                    webpageInstitution="www.swp.com"),
        Institution(idInstitution=3,
                    nameInstitution="Asgard Inc.",
                    webpageInstitution="www.asgard.as"),
        Institution(idInstitution=4,
                    nameInstitution="Blackhole",
                    webpageInstitution="127.0.0.1"),
    ]
    # set SmartContract to Institution
    institutions[0].smartcontract = smartcontracts[0]
    institutions[1].smartcontract = smartcontracts[0]
    institutions[2].smartcontract = smartcontracts[0]
    institutions[3].smartcontract = smartcontracts[0]

    projects: List[Project] = [
        Project(idProject=1,
                nameProject="Computer malt Bild",
                webpageProject="www.cmb.de"),
        Project(idProject=2,
                nameProject="Rangaroek verteidigen",
                webpageProject="www.asgard.as"),
        Project(idProject=3,
                nameProject="Softwareprojekt 2020",
                webpageProject="www.swp.de"),
    ]
    # set SmartContract to Project
    projects[0].smartcontract = smartcontracts[1]
    projects[1].smartcontract = smartcontracts[1]
    projects[2].smartcontract = smartcontracts[1]
    # set Institution to Project
    projects[0].institution = institutions[0]
    projects[1].institution = institutions[2]
    projects[2].institution = institutions[2]

    milestones: List[Milestone] = [
        Milestone(idMilestone=1, goalMilestone=1000, requiredVotesMilestone=112, currentVotesMilestone=112,
                  untilBlockMilestone=600000),
        Milestone(idMilestone=2, goalMilestone=2000, requiredVotesMilestone=112, currentVotesMilestone=12,
                  untilBlockMilestone=1200000),
        Milestone(idMilestone=3, goalMilestone=3000, requiredVotesMilestone=112, currentVotesMilestone=0,
                  untilBlockMilestone=2400000),
        Milestone(idMilestone=4, goalMilestone=1000, requiredVotesMilestone=88, currentVotesMilestone=0,
                  untilBlockMilestone=121212121),
        Milestone(idMilestone=5, goalMilestone=2000, requiredVotesMilestone=88, currentVotesMilestone=12,
                  untilBlockMilestone=321123448),
        Milestone(idMilestone=6, goalMilestone=3000, requiredVotesMilestone=88, currentVotesMilestone=44,
                  untilBlockMilestone=654654832),
        Milestone(idMilestone=7, goalMilestone=5000, requiredVotesMilestone=666, currentVotesMilestone=400,
                  untilBlockMilestone=100000000),
    ]
    # set Project to Milestone
    milestones[0].project = projects[0]
    milestones[1].project = projects[0]
    milestones[2].project = projects[0]
    milestones[3].project = projects[1]
    milestones[4].project = projects[1]
    milestones[5].project = projects[2]
    milestones[6].project = projects[0]

    donations: List[Donation] = [
        Donation(idDonation=1, amountDonation=300),
        Donation(idDonation=2, amountDonation=200),
        Donation(idDonation=3, amountDonation=100),
        Donation(idDonation=4, amountDonation=400),
    ]
    # set Milestone to Donation
    donations[0].milestone = milestones[0]
    donations[1].milestone = milestones[1]
    donations[2].milestone = milestones[2]
    donations[3].milestone = milestones[3]
    # set User to Donation
    donations[0].user = users[0]
    donations[1].user = users[1]
    donations[2].user = users[2]
    donations[3].user = users[3]

    transactions: List[Transaction] = [
        Transaction(idTransaction=1, dateTransaction=datetime.now()),
        Transaction(idTransaction=2, dateTransaction=datetime.now()),
        Transaction(idTransaction=3, dateTransaction=datetime.now()),
        Transaction(idTransaction=4, dateTransaction=datetime.now()),
    ]
    # set smartcontract to transactions
    transactions[0].smartcontract = smartcontracts[0]
    transactions[1].smartcontract = smartcontracts[0]
    transactions[2].smartcontract = smartcontracts[0]
    transactions[3].smartcontract = smartcontracts[0]
    transactions[0].user = users[0]
    transactions[1].user = users[1]
    transactions[2].user = users[2]
    transactions[3].user = users[3]

    vouchers: List[Voucher] = [
        Voucher(idVoucher=1,
                titleVoucher="Von Computer gemaltes Bild",
                descriptionVoucher="Der Computer malt ein täuschend echtes Bild für sie",
                usedVoucher=False,
                untilBlockVoucher=600000000),
        Voucher(idVoucher=2,
                titleVoucher="Software",
                descriptionVoucher="Software für ein Hochschulprojet",
                usedVoucher=False,
                untilBlockVoucher=600000000),
    ]
    # set Institution to Vouchers
    vouchers[0].institution = institutions[0]
    vouchers[1].institution = institutions[0]
    # set Vouchers to Users (and users to vouchers, many-to-many!)
    users[0].vouchers.append(vouchers[0])
    users[1].vouchers.append(vouchers[0])
    users[2].vouchers.append(vouchers[0])
    users[3].vouchers.append(vouchers[0])

    # All objects created, Add and commit to DB:
    objects = [*smartcontracts, *users, *institutions, *projects, *milestones, *vouchers, *transactions,
               *donations]

    for obj in objects:
        session.add(obj)
    session.commit()
