## @package backend.resources.register
#  Handles the register ressources.
#  See rest api documentation for further information.
from flask import (Blueprint, Response, request,jsonify)
from backend.util.db import get_db


bp = Blueprint('institutions', __name__, url_prefix='/api/institutions') # set blueprint name and resource path

## Handles the ressource <base>/sample with GET and POST.
@bp.route('',methods=['GET'])
def register():
    cursor = get_db().cursor()
    test = request.args.get('id', default = 0, type = int)
    if request.method == 'GET': #handle get request on base_url/sample
        cursor.execute('use mydb;') 
        cursor.execute('select idInstitution,nameInstitution,webpageInstitution from institution;') #execute statemant
        version = cursor.fetchall() #fetch database response | see fetchmany(size=x) and fetchall()

        json1=jsonify(version)
        return json1, 201
       #return Response(json1, status=200,mimetype='application/json')
    