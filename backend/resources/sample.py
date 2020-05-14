## @package backend.resources.register
#  Handles the register ressources.
#  See rest api documentation for further information.
from flask import (Blueprint, Response, request)
from backend.util.db import get_db

bp = Blueprint('sample', __name__, url_prefix='/sample') # set blueprint name and resource path

## Handles the ressource <base>/sample with GET and POST.
@bp.route('',methods=['GET','POST'])
def register():
    cursor = get_db().cursor()
    
    if request.method == 'GET': #handle get request on base_url/sample
        cursor.execute('SELECT VERSION()') #execute statemant
        version = cursor.fetchone() #fetch database response | see fetchmany(size=x) and fetchall()
        return Response(version, status=200)
    
    if request.method == 'POST': #handle post request
        # do stuff
        return Response('', status=201)
