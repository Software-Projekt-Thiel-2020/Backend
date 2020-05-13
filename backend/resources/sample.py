## @package backend.resources.register
#  @author Sebastian Steinmeyer
#  Handles the register ressources.
#  See rest api documentation for further information.
import functools
from flask import (Blueprint, Response, request)
from backend.util.db import get_db

bp = Blueprint('sample', __name__, url_prefix='/sample')

## Handles the ressource <base>/register with POST.
@bp.route('',methods=['GET','POST'])
def register():
    db = get_db()
    
    if request.method == 'GET':
        # do stuff
        return Response('', status=200)
    
    if request.method == 'POST':
        # do stuff
        return Response('', status=201)
