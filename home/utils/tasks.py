from home.buckets.bucket import bucket
from celery import shared_task


# TODO : can be async?
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result


@shared_task
def delete_bucket_objects_task(keys):
    bucket.delete_objects(keys)
