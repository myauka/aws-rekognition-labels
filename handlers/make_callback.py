import json
import boto3
import requests


def get_callback_url_from_record(record):
    updated_item = record["dynamodb"]["NewImage"]
    url = updated_item["callback_url"]["S"]
    return url


def get_labels_from_record(record):
    updated_item = record["dynamodb"]["NewImage"]
    labels = updated_item["labels"]["L"]
    return labels


def get_blod_id_from_record(record):
    updated_item = record["dynamodb"]["Keys"]
    blob_id = updated_item["blob_id"]["S"]
    return blob_id


def make_callback(event, context):
    response = {}
    # sent_requests = {}
    for record in event["Records"]:
        if record["eventName"] == "MODIFY":
            response["blob_id"] = get_blod_id_from_record(record)
            response["labels"] = get_labels_from_record(record)
            callback_url = get_callback_url_from_record(record)

            requests.post(callback_url, json=response)

    return {
        "statusCode": 200,
        "body": "Success"
    }
