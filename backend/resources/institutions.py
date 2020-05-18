from flask import (Blueprint, Response, request,json)
from backend.util.db import get_db


bp = Blueprint('institutions', __name__, url_prefix='/api/institutions') # set blueprint name and resource path

@bp.route('',methods=['GET'])
def institutions():
    id = request.args.get('id', default = 0, type = int)
    cursor = get_db().cursor()
    cursor.execute('use mydb;') 
    if(id==0):
      cursor.execute('select idInstitution,nameInstitution,webpageInstitution from institution;')
      data = cursor.fetchall() 
    else:
      cursor.execute('select idInstitution,nameInstitution,webpageInstitution from institution WHERE idInstitution='+str(id)+';') 
      data = cursor.fetchall() 

    names=["id","name","webpage"]
    json_data=[]
    for result in data:
       json_data.append(dict(zip(names,result)))

    jstring = json.dumps(json_data)
    return Response(jstring, status=200,mimetype='application/json')
    