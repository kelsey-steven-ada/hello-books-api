from flask import Blueprint, jsonify, abort, make_response, request, Response
from app.models.author import Author
from .model_services import create_model, get_models_with_filters
from ..db import db

bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

@bp.post("")
def create_author():
    request_body = request.get_json()
    return create_model(Author, request_body)

@bp.get("")
def get_all_authors():
    filters = request.args
    return get_models_with_filters(Author, filters)