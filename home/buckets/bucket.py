import boto3
from django.conf import settings


class Bucket:
    """
    CDN buckets manager
    init method creates connection.

    Note:
        None of these methods are async.
        Use the public interface in the tasks.py module instead.
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
        """Retrieve the list of objects in the S3 bucket."""
        result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        return result.get("Contents", [])

    def delete_objects(self, keys):
        """Delete multiple objects from the S3 bucket."""
        if isinstance(keys, str):
            keys = [keys]
        objects = [{"Key": key} for key in keys]
        self.conn.delete_objects(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Delete={"Objects": objects}
        )
        return True

    def download_objects(self, key):
        """Download an object from the S3 bucket."""
        local_path = f"{settings.AWS_LOCAL_STORAGE}/{key}"
        with open(local_path, "wb") as f:
            self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)

    def upload_objects(self, file_path, key):
        """Upload an object to the S3 bucket."""
        with open(file_path, "rb") as f:
            self.conn.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, key)


bucket = Bucket()
