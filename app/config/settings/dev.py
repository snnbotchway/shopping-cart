from .common import SIMPLE_JWT as COMMON_SIMPLE_JWT
from .common import *

DEBUG = True

SECRET_KEY = "change_me"

ALLOWED_HOSTS = ["*"]

SIMPLE_JWT = {
    **COMMON_SIMPLE_JWT,
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}
