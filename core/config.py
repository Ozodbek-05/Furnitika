from decouple import config, Csv

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# Database
DB_NAME = config('DB_NAME')
DB_PORT = config('DB_PORT')
DB_HOST = config('DB_HOST')
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
