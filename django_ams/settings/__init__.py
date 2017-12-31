import os
from dotenv import load_dotenv
from os.path import join, dirname

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

if os.environ.get('PRODUCTION'):
    from .production import *
else:
    from .development import *
    