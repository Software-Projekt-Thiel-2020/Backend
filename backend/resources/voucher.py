"""Voucher Resource."""
from flask import Blueprint, jsonify

BP = Blueprint('voucher', __name__, url_prefix='/api/voucher')


@BP.route('', methods=['GET'])
def voucher_get():
    """
    Handles GET for resource <base>/api/voucher .

    :return: json data of projects
    """
    return jsonify({'status': 'TODO: create route'})


@BP.route('', methods=['DELETE'])
def voucher_delete():
    """
    Handles DELETE for resource <base>/api/voucher .

    :return: json data of projects
    """
    return jsonify({'status': 'TODO: create route'})


@BP.route('/requests', methods=['GET'])
def voucher_requests_get():
    """
    Handles GET for resource <base>/api/voucher/requests .

    :return: json data of projects
    """
    return jsonify({'status': 'TODO: create route'})


@BP.route('/requests', methods=['POST'])
def voucher_requests_post():
    """
    Handles POST for resource <base>/api/voucher/requests .

    :return: json data of projects
    """
    return jsonify({'status': 'TODO: create route'})


@BP.route('/requests', methods=['DELETE'])
def voucher_requests_delete():
    """
    Handles DELETE for resource <base>/api/voucher/requests .

    :return: json data of projects
    """
    return jsonify({'status': 'TODO: create route'})
