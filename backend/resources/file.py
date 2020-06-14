import json
import os
import uuid
from typing import List

import validators
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from werkzeug.utils import secure_filename

from backend.database.db import DB_SESSION
from backend.database.model import Milestone, Institution
from backend.database.model import Project
from backend.resources.helpers import auth_user, check_params_int

BP = Blueprint('file', __name__, url_prefix='/api/file')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


# TODO satisfy linter
@BP.route('', methods=['POST'])
def file_upload():
	"""
    Handles uploading a file for  .

    :return: json data of projects
    """
	
	id_inst = request.headers.get('idInstitution')
	id_proj = request.headers.get('idProject')

	if id_inst is None and id_proj is None:
		return jsonify({'error':'No project/institution given'})
	
	if 'file' not in request.files:
		return jsonify({'error':'No file given'})

	file = request.files['file']
	
	if file.filename == '':
		return jsonify({'error':'No file given'})

	if not (file and allowed_file(file.filename)):
		return jsonify({'error':'File extension not allowed'})

	# Generate a new filename until on that isnt already taken is given
	while True:
		n_filename = str(uuid.uuid4()) + file.filename.split(".")[1]

		if n_filename not in os.listdir(current_app.config['UPLOAD_FOLDER']):
			break

	file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], "."+n_filename))

	# TODO add picture to Institution/Project

	return jsonify({'status':'ok'}), 201


@BP.route('/<filename>', methods=['GET'])
def file_get(filename):
	return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)