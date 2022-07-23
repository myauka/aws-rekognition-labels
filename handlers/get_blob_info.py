import os
import json
import boto3

TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb_client = boto3.client("dynamodb")


def get_item_from_dynamodb(blob_id):
    try:
        item = dynamodb_client.get_item(
            TableName=TABLE_NAME,
            Key={
                "blob_id": {
                    "S": blob_id
                }
            }
        ).get("Item")
    except:
        return None

    return item


def get_blob_info(event, context):
    response = {}

    blob_id = event["pathParameters"]["blob_id"]
    item = get_item_from_dynamodb(blob_id)

    if not item:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "blob is not found"})
        }

    response["blob_id"] = item["blob_id"]["S"]
    response["labels"] = item["labels"]["L"]

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
