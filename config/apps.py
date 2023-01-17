from decouple import config

CORS_ORIGINS = str(config('CORS_ORIGINS', default='*')).split(',')

APP_NAME = config('APP_NAME', default='app')
DEBUG = config('DEBUG', cast=bool, default=False)
API_DEBUG = config('API_DEBUG', cast=bool, default=False) and DEBUG

AUTH_APP_NAME = config('AUTH_APP_NAME', default=APP_NAME)
AUTH_APP_PORT = config('AUTH_APP_PORT', cast=int, default=8000)
AUTH_APP_HOST = config('AUTH_APP_HOST', default='0.0.0.0')
SECRET_KEY = config('SECRET_KEY', default='a')
EXPIRED_TIME = config('EXPIRED_TIME', cast=int, default=60)

MANAGEMENT_APP_NAME = config('MANAGEMENT_APP_NAME', APP_NAME)
MANAGEMENT_APP_PORT = config('MANAGEMENT_APP_PORT', cast=int, default=8001)
MANAGEMENT_APP_HOST = config('MANAGEMENT_APP_HOST', default='0.0.0.0')
