from uuid import uuid4

from decouple import config

MONGO_URI = config('MONGO_URI', default=None)
MONGO_DB = config('MONGO_DB', default=None)

GENERAL_MONGO_CONFIG = {
    'hash': str(uuid4()),
    'uri': MONGO_URI,
    'db': MONGO_DB
}

MANAGEMENT_DB_URI = config('MANAGEMENT_DB_URI', default=MONGO_URI)
MANAGEMENT_MONGO_DB = config('MANAGEMENT_MONGO_DB', default=MONGO_DB)

MANAGEMENT_MONGO_CONFIG = {
    'hash': str(uuid4()),
    'uri': MANAGEMENT_DB_URI,
    'db': MANAGEMENT_MONGO_DB
}
