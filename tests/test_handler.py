import os
import pytest
import json
from unittest.mock import patch, MagicMock
from lambda_function import handler

os.environ["TABLE_NAME"] = "TestTable"

VALID_EVENT = {
    "body": json.dumps({
        "messageUUID": "123e4567-e89b-12d3-a456-426614174000",
        "messageText": "This is a valid message.",
        "messageDatetime": "2025-06-01 12:30:00"
    })
}

INVALID_EVENT_SHORT_MSG = {
    "body": json.dumps({
        "messageUUID": "uuid",
        "messageText": "Short",
        "messageDatetime": "2025-06-01 12:30:00"
    })
}

INVALID_EVENT_NO_BODY = {}

@patch("lambda_function.handler.boto3.resource")
def test_valid_event(mock_dynamodb_resource):
    mock_table = MagicMock()
    mock_dynamodb_resource.return_value.Table.return_value = mock_table

    response = handler.lambda_handler(VALID_EVENT, {})
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert "Message saved successfully" in body["message"]
    mock_table.put_item.assert_called_once()

@patch("lambda_function.handler.boto3.resource")
def test_invalid_message_text(mock_dynamodb_resource):
    response = handler.lambda_handler(INVALID_EVENT_SHORT_MSG, {})
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "messageText must be a string between 10 and 100 characters" in body["error"]

@patch("lambda_function.handler.boto3.resource")
def test_missing_body(mock_dynamodb_resource):
    response = handler.lambda_handler(INVALID_EVENT_NO_BODY, {})
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "Missing request body" in body["error"]
