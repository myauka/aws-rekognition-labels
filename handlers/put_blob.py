import os
import json
import uuid
import boto3

BUCKET_NAME = os.environ["BUCKET_NAME"]
TABLE_NAME = os.environ["TABLE_NAME"]

s3_client = boto3.client("s3")
dynamodb_client = boto3.client("dynamodb")


def main(event, context):
    callback_url = json.loads(event["body"]).get("callback_url")

    blob_id = str(uuid.uuid4())

    upload_url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': blob_id
            },
            ExpiresIn=300
        )

    dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item={
            "blob_id": {"S": blob_id},
            "callback_url": {"S", callback_url},
            "upload_url": {"S", upload_url}
        }
    )

    return {
        "statusCode": 201,
        "body": json.dumps({
            "blob_id": blob_id,
            "callback_url": callback_url,
            "upload_url": upload_url
        })
    }
