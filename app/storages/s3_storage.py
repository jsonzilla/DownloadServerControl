import logging
import boto3
from botocore.exceptions import ClientError


def create_presigned_url(bucket_name: str, object_name: str, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name},
            ExpiresIn=expiration
        )

    except ClientError as e:
        logging.error(e)
        return None

    return response
