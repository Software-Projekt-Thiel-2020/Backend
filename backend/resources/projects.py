from flask import(Blueprint, Response, request, json)
from backend.util.db import get_db

bp = Blueprint('projects', __name__, url_prefix='/api/projects') #set blueprint name and resource path

## Handles the ressource <base>/api/projects with GET and POST.
@bp.route('',methods=['GET'])
def projects():
    error = None
    args = request.args
    if request.method == 'GET':
        cursor = get_db().cursor()
        id = args.get('id')
        instid = args.get('idinstitution')
        cursor.execute('use mydb')
        resp = None
        if id is not None and instid is not None:
            cursor.execute('select * from project where idProject = %s and fkInstitutionProject = %s', (id, instid))
        elif id is not None and instid is None:
            cursor.execute('select * from project where idProject = %s', (id,))
        elif id is None and instid is not None:
            cursor.execute('select * from project where idProject = %s and fkInstitutionProject = %s', (instid,))
        else:
            cursor.execute('select * from project')
        
        json_data = []
        json_names = ['id', 'name', 'webpage', 'idsmartcontract', 'idinstitution']
        for result in cursor:
            json_data.append(dict(zip(json_names,result)))

        json_str = json.dumps(json_data)
        return Response(json_str, status=200, mimetype='application/json')
        
    else:
        abort(400)