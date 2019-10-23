KEY_ID = None
TEAM_ID = None
SECRET_KEY_FILE = None

# Load custom development settings overrides
try:
    from local_settings import *
except:
    pass