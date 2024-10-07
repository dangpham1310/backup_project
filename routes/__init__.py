from flask import Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


routes = Blueprint('routes', __name__)

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",  # Redis URI
    default_limits=["20000 per day", "50 per hour"]
)

from .db import *
from .home import *
from .login import *
from .menu import *
from .student import *




