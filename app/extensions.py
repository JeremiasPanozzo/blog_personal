# extensions.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Limita por IP con límites por defecto (ajústalos a tu gusto)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
