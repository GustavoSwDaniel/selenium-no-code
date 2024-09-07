import os

class Config:
    URL_TEST = os.getenv('URL_TEST', 'https://www.techsolutio.com')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:t8ltavvRLd@127.0.0.1:5432/postgres')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'enowshopv2')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME', 'us-east-1'
