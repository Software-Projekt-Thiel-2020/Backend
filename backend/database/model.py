"""Defines the (declarative_base) model."""
from datetime import datetime
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, BINARY, BOOLEAN, DateTime, Float, TEXT
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import relationship

BASE: DeclarativeMeta = declarative_base()


class Project(BASE):
    __tablename__ = 'Project'
    idProject = Column(Integer, primary_key=True)
    nameProject = Column(VARCHAR(256))
    webpageProject = Column(VARCHAR(256))
    picPathProject = Column(VARCHAR(256))
    descriptionProject = Column(TEXT)

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
    addressInstitution = Column(VARCHAR(256))
    picPathInstitution = Column(VARCHAR(256))
    latitude = Column(Float)
    longitude = Column(Float)
    descriptionInstitution = Column(TEXT)

    projects = relationship("Project", back_populates="institution")

    smartcontract_id = Column(Integer, ForeignKey('SmartContract.idSmartContract'))
    smartcontract = relationship("SmartContract", back_populates="institutions")

    user_id = Column(Integer, ForeignKey('User.idUser'))
    user = relationship("User", back_populates="institution")

    vouchers = relationship("Voucher", back_populates="institution")
    publickeyInstitution = Column(VARCHAR(64))


class Voucher(BASE):
    __tablename__ = 'Voucher'
    idVoucher = Column(Integer, primary_key=True)
    titleVoucher = Column(VARCHAR(32))
    descriptionVoucher = Column(VARCHAR(1024))
    priceVoucher = Column(Integer, nullable=False)
    available = Column(BOOLEAN, default=True)
    validTime = Column(Integer, default=2 * 31536000)

    institution_id = Column(Integer, ForeignKey('Institution.idInstitution'))
    institution = relationship("Institution", back_populates="vouchers")

    users = relationship("VoucherUser")


class User(BASE):
    __tablename__ = 'User'
    idUser = Column(Integer, primary_key=True)
    usernameUser = Column(VARCHAR(45))
    firstnameUser = Column(VARCHAR(45))
    lastnameUser = Column(VARCHAR(45))
    emailUser = Column(VARCHAR(45))
    publickeyUser = Column(VARCHAR(64))
    privatekeyUser = Column(BINARY(128))
    authToken = Column(VARCHAR(2048))
    group = Column(VARCHAR(32))

    donations = relationship("Donation", back_populates="user")

    transactions = relationship("Transaction", back_populates="user")

    vouchers = relationship("VoucherUser")

    institution = relationship("Institution", back_populates="user")


class VoucherUser(BASE):
    __tablename__ = "VoucherUser"
    idVoucherUser = Column(Integer, primary_key=True)
    id_voucher = Column(Integer, ForeignKey('Voucher.idVoucher'))
    id_user = Column(Integer, ForeignKey('User.idUser'))
    usedVoucher = Column(BOOLEAN)
    expires_unixtime = Column(DateTime)

    voucher = relationship("Voucher", back_populates="users")
    user = relationship("User", back_populates="vouchers")


class Donation(BASE):
    __tablename__ = 'Donation'
    idDonation = Column(Integer, primary_key=True)
    amountDonation = Column(Integer)
    voteDonation = Column(BOOLEAN)

    user_id = Column(Integer, ForeignKey('User.idUser'))
    user = relationship("User", back_populates="donations")

    milestone_id = Column(Integer, ForeignKey('Milestone.idMilestone'))
    milestone = relationship("Milestone", back_populates="donations")


class Transaction(BASE):
    __tablename__ = 'Transaction'
    idTransaction = Column(Integer, primary_key=True)
    dateTransaction = Column(DateTime)

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
             publickeyUser='0xB8331Dcd8693F69f091A9E4648A5a8ee89226CE3',
             privatekeyUser=b'\xf5\x11\xdd\xc9\x17\xb4F\xd7\x1d\x84\x02\xe2\xc1[\x166\xd3\xf5\xd5\xd5\x9a\xcf\xc1Q'
                            b'y\x11\xf9\x93\xbd\n\xfdu'),
        User(idUser=2,
             usernameUser="MSDOSManfred",
             firstnameUser="Manfred", lastnameUser="MSDOS",
             emailUser="msdosm@swp.de",
             publickeyUser='0x4ad351026d561E94870D7091367992efFb3Ee75B',
             privatekeyUser=b'Tg\xcaj\xcf\xad\xbb\x98\xdek+\r\t\xb3\xe8d\xe2\xf5,([\x03D<.wm>\xf1\x84\xef\xc3'),
        User(idUser=3,
             usernameUser="HardwareHansPeter",
             firstnameUser="HansPeter", lastnameUser="Hardware",
             emailUser="hwhp@swp.de",
             publickeyUser='0xCbC8928Cf40b02ed7db3C3c68C1399aD1E464856',
             privatekeyUser=b'-\xa2\x99\xbdk(\xbd\xfb\xc7\xae8\xcc\xf1\rr\xd1\x88\xb6\x14&\x0f\x92\xf8\x8c:'
                            b'u\xf5D\xe9,\x0b\x86'),
        User(idUser=4,
             usernameUser="BIOSBernhard",
             firstnameUser="Bernhard", lastnameUser="BIOS",
             emailUser="biosb@swp.de",
             publickeyUser='0xb8fE165e28EeE26c87470575d1fCFf0EDcA8c10E',
             privatekeyUser=b'%|\x87+\x0fOL<w[\xd9 6\x81\xc2k=@(\xb9z\x1e\x14\x07\x86\xaf\xb2:\x96<6L'),
        User(idUser=5,
             usernameUser="OdinsonThor",
             firstnameUser="Thor", lastnameUser="Odinson",
             emailUser="ot@swp.de",
             publickeyUser='0x93c31008E4395C75D3Fa332445433bf5f987Cf21',
             privatekeyUser=b'v\xc1\xf8\x8a;\x06\xd5bo\x16L\xa9\x87N\xd6+-\xc4Vn z&\x9e{\xb7\x94\xe7C)\xed\xb6'),
        User(idUser=6,
             usernameUser="sw2020testuser1.id.blockstack",
             firstnameUser="testuser1", lastnameUser="sw2020",
             emailUser="testuser1@example.com",
             publickeyUser='0x865fefF6a8503405f8a316e53039dc8332a5A60b',
             privatekeyUser=b'/8\x9f}\x96\xe9{\xee\x14\x972\x01b\xf3\xb6/\xbcjX\x19J\xfbgW\xd6\x94p\xda\xa6/=\xdf',
             authToken=TOKEN_1,
             group="support"),
        User(idUser=7,
             usernameUser="sw2020testuser2.id.blockstack",
             firstnameUser="testuser2", lastnameUser="sw2020",
             emailUser="testuser2@example.com",
             publickeyUser='0x7Dca2Ba711f089C608ABe8C6F59Fe7B5F84fced8',
             privatekeyUser=b'\x02P\x13\x96\xdc\xae\x86\x86\xff\x86\x83)Hj\xf1\x1c\x94\xc7?\xabj'
                            b'\xda\x93\t\xc0\xe8\xe4\t\xde\xd1M\xaf',
             authToken=TOKEN_2),
    ]

    institutions: List[Institution] = [
        Institution(idInstitution=1,
                    nameInstitution="MSGraphic",
                    webpageInstitution="www.msgraphic.com",
                    addressInstitution="Address1",
                    publickeyInstitution="0xE92F05FEe101648aE33169150feE8F28FeFc19C2",
                    # key = b',\xc5p\xc97Ue\x9d\x88\xbakd\xb4\xdbb\xdc\xb80\xa6\x9be\x0c\xf0\xdeX\xee\xa61F_\x13~'
                    latitude=52.030228,
                    longitude=8.532471,
                    picPathInstitution="a49d11ef-eb29-4867-9254-7c1ef1a7870c.png",
                    descriptionInstitution="# MSGraphic\n'MSGraphic is the best company ever' - Donald Trump"),
        Institution(idInstitution=2,
                    nameInstitution="SWP",
                    webpageInstitution="www.swp.com",
                    addressInstitution="Address2",
                    publickeyInstitution="0x4b90030b0BA6790E8A34f5f58f10a43B3D13dCD1",
                    # key = b"\xc6$\xf2\xe6\x81a7\rh`\xb0\x86I\x7f\x1e%8v\xde[\xb8w\x8c7\xf4'\xc3z\xb9g\x17\xb1"
                    latitude=40.712776,
                    longitude=-74.005974,
                    picPathInstitution="0984d9d5-7ebc-45a5-9258-46fe2c2b4151.png",
                    descriptionInstitution="# SWP\nSoftwareprojekt202"),
        Institution(idInstitution=3,
                    nameInstitution="Asgard Inc.",
                    webpageInstitution="www.asgard.as",
                    addressInstitution="Address3",
                    publickeyInstitution="0xC6f1F12B6df34C98E670531Ab3cdA01df26Db585",
                    # key = b'g\xbef\xb0\xc6\x04\xa3i%P\x03\xb7\xbe\xac\xc0}rN\xeaq\xc9\x9b\x88j\x04m\x15\xcah\xb4\xf1-'
                    latitude=-13.531950,
                    longitude=-71.967461,
                    picPathInstitution="88c0bc0a-c673-4cdf-8216-cd4e2c916be2.png",
                    descriptionInstitution="# Asgard Inc.\nWir sind die, die Asgard kennen wie kein anderer!"),
        Institution(idInstitution=4,
                    nameInstitution="Blackhole",
                    webpageInstitution="127.0.0.1",
                    addressInstitution="Address4",
                    publickeyInstitution="0x03bD157AF2BA8437CaB84bF3383d918f0a993399",
                    # key = b'"\x1e\xe6\x01mu\xf07\xed\x84\xc1\xeb\x9du\x90\x1b\x80f\xc6g\x814+\xc3o.<9\xa7S\xb7M'
                    latitude=42.267502,
                    longitude=2.960840,
                    picPathInstitution="cdbad6a3-4322-43b3-9c07-be3606508386.png",
                    descriptionInstitution="# Blackhole\nBlackhole international is the company you can trust with all "
                                           "your security needs!"),
    ]
    # set SmartContract to Institution
    institutions[0].smartcontract = smartcontracts[0]
    institutions[1].smartcontract = smartcontracts[0]
    institutions[2].smartcontract = smartcontracts[0]
    institutions[3].smartcontract = smartcontracts[0]

    institutions[0].user = users[4]
    institutions[1].user = users[3]
    institutions[2].user = users[2]
    institutions[3].user = users[1]

    projects: List[Project] = [
        Project(idProject=1,
                nameProject="Computer malt Bild",
                webpageProject="www.cmb.de",
                picPathProject="c3637aac-145a-4942-96f4-34bbefb48689.png",
                descriptionProject="# Computer malt Bild\nDer Computer malt ein Bild für Sie!"),
        Project(idProject=2,
                nameProject="Rangaroek verteidigen",
                webpageProject="www.asgard.as",
                picPathProject="182713b2-1862-416f-bfc9-b07b952c0bea.png",
                descriptionProject="# Rangaroek verteidigen\nRangaroek muss verteidigt werden!"),
        Project(idProject=3,
                nameProject="Softwareprojekt 2020",
                webpageProject="www.swp.de",
                picPathProject="4eb9a451-2be6-4f98-bb62-3d5673d0c120.png",
                descriptionProject="# Softwareprojekt 2020\nDies ist eine sehr ausführliche Beschreibung!"),
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
        Donation(idDonation=1, amountDonation=300, voteDonation=True),
        Donation(idDonation=2, amountDonation=200, voteDonation=False),
        Donation(idDonation=3, amountDonation=100, voteDonation=True),
        Donation(idDonation=4, amountDonation=400, voteDonation=False),
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
                priceVoucher=1000,
                available=False,
                ),
        Voucher(idVoucher=2,
                titleVoucher="Software",
                descriptionVoucher="Software für ein Hochschulprojet",
                priceVoucher=2000,
                available=True,
                ),
    ]

    associations: List[VoucherUser] = [
        VoucherUser(idVoucherUser=1,
                    usedVoucher=False,
                    expires_unixtime=datetime(2020, 1, 1)),
        VoucherUser(idVoucherUser=2,
                    usedVoucher=False,
                    expires_unixtime=datetime(2022, 5, 17)),
        VoucherUser(idVoucherUser=3,
                    usedVoucher=False,
                    expires_unixtime=datetime(2022, 1, 13)),
        VoucherUser(idVoucherUser=4,
                    usedVoucher=True,
                    expires_unixtime=datetime(2021, 5, 17)),
    ]

    # set Institution to Vouchers
    vouchers[0].institution = institutions[0]
    vouchers[1].institution = institutions[0]

    # set Vouchers to Users (and users to vouchers, many-to-many!)
    associations[0].voucher = vouchers[0]
    associations[1].voucher = vouchers[1]
    associations[2].voucher = vouchers[0]
    associations[3].voucher = vouchers[1]

    users[0].vouchers.append(associations[0])
    users[1].vouchers.append(associations[1])
    users[5].vouchers.append(associations[2])
    users[6].vouchers.append(associations[3])

    # All objects created, Add and commit to DB:
    objects = [*smartcontracts, *users, *institutions, *projects, *milestones, *vouchers, *transactions,
               *donations]

    for obj in objects:
        session.add(obj)
    session.commit()
