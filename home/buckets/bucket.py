import boto3
from django.conf import settings


class Bucket:
    """
    CDN buckets manager
    init method creates connection.

    Note:
        none of these methods are async.
        use public interface in tasks.py module instead.
    """

    def __init__(self):
        session = boto3.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVER_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

    def get_objects(self):
        result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result["KeyCount"]:
            return result["Contents"]
        else:
            return None

    def delete_objects(self, keys):
        self.conn.delete_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=keys)
        return True

    # def download_objects(self, keys):
    #     self.conn.download_file(
    #         Bucket=settings.AWS_STORAGE_BUCKET_NAME,
    #         Key=keys,
    #         Filename=settings.MEDIA_ROOT + keys,
    #     )
    #     return True


bucket = Bucket()
