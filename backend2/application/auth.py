from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims["is_administrator"]:
            return fn(*args, **kwargs)
        else:
            return jsonify(msg="Admins only!"), 403

    return decorator