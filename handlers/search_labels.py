import os
import json
import boto3
import urllib.parse

BUCKET_NAME = os.environ["BUCKET_NAME"]
TABLE_NAME = os.environ["TABLE_NAME"]

s3_client = boto3.client("s3")
dynamodb_client = boto3.client("dynamodb")
rekognition_client = boto3.client("rekognition")


def add_labels_to_item(blob_id, labels):
    dynamodb_client.update_item(
        TableName=TABLE_NAME,
        Key={
            "blob_id": {
                "S": blob_id
            }
        },
        AttributeUpdates={
            "labels": {
                "Action": "ADD",
                "Value": {"L", labels}
            }
        }
    )


def extract_labels_from_blob(blob_id):
    rekognition_results = rekognition_client.detect_labels(Image={
        "S3Object": {"Bucket": BUCKET_NAME, "Name": blob_id}
    })
    extracted_labels = json.loads(rekognition_results)["Labels"]
    return extracted_labels


def process_blob(event, context):
    blob_id = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")

    labels = extract_labels_from_blob(blob_id)

    add_labels_to_item(blob_id, labels)

    return {
        "statusCode": 200,
        "body": "Success"
    }


