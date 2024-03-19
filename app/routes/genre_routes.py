from flask import Blueprint, jsonify, abort, make_response, request, Response
from app.models.genre import Genre
from .model_services import create_model, get_models_with_filters, validate_model

bp = Blueprint("genres_bp", __name__, url_prefix="/genres")

@bp.post("")
def create_genre():
    request_body = request.get_json()
    return create_model(Genre, request_body)

@bp.get("")
def get_all_genres():
    filters = request.args
    return get_models_with_filters(Genre, filters)