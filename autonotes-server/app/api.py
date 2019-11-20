from flask import Blueprint
from flask_restplus import Api
from .apis.spots import ns as spots
# from .apis.RESOURCE import ns as RESOURCE
from .helper.authentication import authorizations

blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0', title='YOUR API',
    description='***',
    authorizations=authorizations
)

api.add_namespace(spots)
# api.add_namespace(RESOURCE)