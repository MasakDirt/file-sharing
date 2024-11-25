from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel

from src.settings import CSRF_SECRET_KEY


class CsrfSettings(BaseModel):
    secret_key: str = CSRF_SECRET_KEY


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()
