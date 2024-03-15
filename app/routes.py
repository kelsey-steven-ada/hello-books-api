from flask import Blueprint, jsonify, abort, make_response, request, Response
from app.models.book import Book
from sqlalchemy import select
from .db import db

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.post("")
def create_book():
    request_body = request.get_json()

    try:
        new_book = Book.from_dict(request_body)
        
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_book)
    db.session.commit()

    return make_response(new_book.to_dict(), 201)

@books_bp.get("")
def get_all_books():
    query = db.select(Book)

    # If we have a `title` query parameter, we can add on to the query object
    title_param = request.args.get("title")
    if title_param:
        # Match the title_param exactly, including capitalization
        # query = query.where(Book.title == title_param)

        # If we want to allow partial matches, we can use the % wildcard with `like()`
        # If `title_param` contains "Great", the code below will match 
        # both "The Great Gatsby" and "Great Expectations"
        # query = query.where(Book.title.like(f"%{title_param}%"))

        # If we want to allow searching case-insensitively, 
        # we could use ilike instead of like
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    # If we have other query parameters, we can continue adding to the query
    description_param = request.args.get("description")
    if description_param:
        # In case there are books with similar titles, we can also filter by description
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    books = db.session.scalars(query.order_by(Book.id))
    # We could also write the line above as:
    # books = db.session.execute(query).scalars()

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return jsonify(books_response)

@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)

    return book.to_dict()

@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body.get("title")
    book.description = request_body.get("description")
    db.session.commit()

    return Response(status=204)

@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()

    return Response(status=204)

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return model
