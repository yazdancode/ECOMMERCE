from celery import shared_task

from home.buckets.bucket import bucket


# TODO : can be async?
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result


@shared_task
def delete_bucket_objects_task(keys):
    bucket.delete_objects(keys)


@shared_task
def download_objects_task(keys):
    bucket.download_objects(keys)


@shared_task
def upload_objects_task(file_path, key):
    bucket.upload_objects(file_path, key)
