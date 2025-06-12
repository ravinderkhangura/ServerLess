import os
import json
import logging
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# TABLE_NAME = os.environ.get("TABLE_NAME")
# dynamodb = boto3.resource("dynamodb")
# table = dynamodb.Table(TABLE_NAME)

def validate_event(event):
    required_fields = {"messageUUID", "messageText", "messageDatetime"}

    if not required_fields.issubset(event):
        raise ValueError("Missing required fields in input.")

    message_text = event["messageText"]
    if not isinstance(message_text, str) or not (10 <= len(message_text) <= 100):
        raise ValueError("messageText must be a string between 10 and 100 characters.")

    try:
        datetime.strptime(event["messageDatetime"], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("messageDatetime must be in 'YYYY-MM-DD HH:MM:SS' format.")

    return event

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        body = event.get("body")
        if body is None:
            raise ValueError("Missing request body.")

        message = json.loads(body)
        valid_data = validate_event(message)
        table_name = os.environ.get("TABLE_NAME")
        if not table_name:
            raise ValueError("TABLE_NAME environment variable not set.")

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)
        
        table.put_item(Item=valid_data)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Message saved successfully!"})
        }

    except (ValueError, ClientError) as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }

    except Exception as e:
        logger.exception("Unhandled exception occurred.")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }
