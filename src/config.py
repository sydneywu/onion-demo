import os
import secrets
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    POSTGRES_CONNECTION_STRING: str
    POSTGRES_SYNC_CONNECTION_STRING: str
    SECRET_KEY: str = secrets.token_urlsafe(32)

    class Config:
        case_sensitive = True
        env_file = os.path.join(Path(__file__).resolve().parent.parent, '.env')

def get_settings():
    # Set env to the value of PYTHON_ENV, defaulting to None if not set
    env = os.getenv('PYTHON_ENV')
    env_file = os.path.join(Path(__file__).resolve().parent.parent, '.env')

    if env == 'test':  # Switch to '.env.test' if PYTHON_ENV is 'test'
        env_file = '.env.test'

    return Settings(_env_file=env_file)

settings = get_settings()
