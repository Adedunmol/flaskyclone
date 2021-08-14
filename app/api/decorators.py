from app.api.errors import forbidden
from flask import g
from functools import wraps

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient Perissions')
            return f(*args, **kwargs)
        return decorated
    return decorator