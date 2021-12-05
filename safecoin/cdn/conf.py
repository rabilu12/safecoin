import os
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "charityland"
AWS_S3_ENDPOINT_URL = "https://fra1.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_DEFAULT_ACL = "public-read"

AWS_LOCATION = "https://charityland.fra1.digitaloceanspaces.com"
STATICFILES_STORAGE = "StaticRootS3Boto3Storage"
DEFAULT_FILE_STORAGE = "safecoin.cdn.backends.MediaRootS3Boto3Storage"

STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, 'static')  
STATIC_ROOT = STATIC_ROOT = BASE_DIR / "staticfiles-cdn" # dev example

MEDIA_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, 'media') 
MEDIA_ROOT = 'media/'
