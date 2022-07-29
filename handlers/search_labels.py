import os
import json
import boto3
import urllib.parse

BUCKET_NAME = os.environ["BUCKET_NAME"]
TABLE_NAME = os.environ["TABLE_NAME"]

s3_client = boto3.client("s3")
dynamodb_client = boto3.client("dynamodb")
rekognition_client = boto3.client("rekognition", "us-east-1")


def add_labels_to_item(blob_id, labels: list):
    # list_of_labels = []
    # for label in labels:
    #     formatted_label = {"Name": {"S": label["Name"]}, "Confidence": {"N": label["Confidence"]},
    #                        "Instances": {"L": label["Instances"]}, "Parents": {"L": label["Parents"]}}
    #     list_of_labels.append("S": formatted_label)
    converted_to_str_labels = str(labels)[1:-1]
    dynamodb_client.update_item(
        TableName=TABLE_NAME,
        Key={
            "blob_id": {
                "S": blob_id
            }
        },
        UpdateExpression="SET #labels = :extracted_labels",
        ExpressionAttributeNames={
            "#labels": "labels"
        },
        ExpressionAttributeValues={
            ":extracted_labels": {"S": converted_to_str_labels}
        }
        # AttributeUpdates={
        #     "labels": {
        #         "Action": "ADD",
        #         "Value": {"S": converted_to_str_labels}
        #     }
        # }
    )


# def extract_labels_from_blob(blob_id):
#     rekognition_results = rekognition_client.detect_labels(Image={
#         "S3Object": {"Bucket": BUCKET_NAME, "Name": blob_id}
#     })
#     extracted_labels = json.loads(rekognition_results)["Labels"]
#     return extracted_labels


def process_blob(event, context):
    blob_id = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")

    print(blob_id)
    rekognition_results = rekognition_client.detect_labels(Image={
        "S3Object": {"Bucket": BUCKET_NAME, "Name": blob_id}
    })
    labels = rekognition_results["Labels"]
    # labels = extract_labels_from_blob(f'{blob_id}.jpeg')

    add_labels_to_item(blob_id.split(".")[0], labels)

    return {
        "statusCode": 200,
        "body": "Success"
    }
