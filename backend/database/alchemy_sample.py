import configparser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import alchemy_decl as ad

CFG_PARSER = configparser.ConfigParser()
CFG_PARSER.read("../../backend_config.ini")  # run this script as local py file to let the path work

# set the configuration of the database connection
DB_CONFIG = {
    'user': CFG_PARSER["Database"]["USER"],
    'password': CFG_PARSER["Database"]["PASSWORD"],
    'host': CFG_PARSER["Database"]["HOST"],
}

db_uri = 'mysql+pymysql://' + DB_CONFIG['user'] + ':' + DB_CONFIG['password'] + '@' + DB_CONFIG['host'] + '/mydb'

engine = create_engine(db_uri)
print(engine.table_names())

Session = sessionmaker(bind=engine)
session = Session()

for project in session.query(ad.Project):
    print(project.idProject, project.nameProject)
