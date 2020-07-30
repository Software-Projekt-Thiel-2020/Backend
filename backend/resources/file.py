import os
import uuid
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from sqlalchemy.orm.exc import NoResultFound

from backend.database.model import Institution
from backend.database.model import Project
from backend.resources.helpers import auth_user, db_session_dec

BP = Blueprint('file', __name__, url_prefix='/api/file')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


# TODO satisfy linter
@BP.route('', methods=['POST'])
@auth_user
@db_session_dec
def file_upload(session, user_inst):  # pylint:disable=unused-argument, too-many-branches
    """
    Handles uploading a file for  .

    :return: json data of projects
    """
    # ToDo: check permissions
    id_inst = request.headers.get('idInstitution')
    id_proj = request.headers.get('idProject')

    if id_inst is None and id_proj is None:
        return jsonify({'error': 'No project/institution given'}), 400

    if id_inst is not None:
        inst: Institution = session.query(Institution).filter(Institution.idInstitution == id_inst). \
            filter(Institution.user == user_inst).one_or_none()
        if inst is None:
            return jsonify({'error': 'No Institution found'}), 404

    if id_proj is not None:
        proj: Project = session.query(Project).join(Project.institution).filter(Project.idProject == id_proj). \
            filter(Institution.user == user_inst).one_or_none()
        if proj is None:
            return jsonify({'error': 'No Project found'}), 404

    if 'file' not in request.files:
        return jsonify({'error': 'No file given'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file given'}), 400

    if not (file and allowed_file(file.filename)):
        return jsonify({'error': 'File extension not allowed'}), 403

    # Generate a new filename until on that isnt already taken is given
    while True:
        n_filename = str(uuid.uuid4()) + "." + file.filename.split(".")[1]

        if n_filename not in os.listdir(current_app.config['UPLOAD_FOLDER']):
            break

    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], n_filename))

    try:
        if inst is not None:
            inst.picPathInstitution = n_filename
            session.add(inst)

        if proj is not None:
            proj.picPathProject = n_filename
            session.add(proj)

    except NoResultFound:
        return jsonify(), 404

    session.commit()

    return jsonify({'status': 'ok'}), 201


@BP.route('/<filename>', methods=['GET'])
def file_get(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
