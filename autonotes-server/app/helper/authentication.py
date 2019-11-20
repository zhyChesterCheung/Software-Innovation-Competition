from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

tkauth = HTTPTokenAuth(scheme='JWT')
@tkauth.verify_token
def verify_token(token):
    pass

auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(id, password):
    pass

authorizations = {
    'basic': {
        'type': 'basic',
        'description': '基本认证'
        },
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': '密钥认证'
    },
}