
from flask import Blueprint
bp = Blueprint('file', __name__, url_prefix='/file')

from backupclient.File import routes