from flask import Blueprint

blueprint = Blueprint(
    'pestmanagement_blueprint',
    __name__,
    url_prefix='/harvesta-api/pestmanagement'
)
