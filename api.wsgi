import os
import sys

sys.path.insert(0, '/app/awdb_api')
os.environ['API_ROOT'] = "/api"
from api import app as application