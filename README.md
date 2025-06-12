# 📨 Message Processor - Serverless Solution (AWS CDK + Docker Lambda)

This project implements a serverless message ingestion service using AWS CDK (Python) with a Docker-based Lambda function. It accepts messages via API Gateway, validates them, and stores them in DynamoDB.

## Features

- AWS Lambda (DockerImageFunction)
- API Gateway (POST endpoint)
- DynamoDB table with messageUUID as partition key
- Input validation and error handling
- Logging with Python's logging module
- Unit tests with pytest

## Setup & Deployment on windows machine

1. Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1     
pip install -r requirements.txt
```
Use - "powershell -ExecutionPolicy Bypass" on windows


2. Bootstrap your AWS environment

```bash
cdk bootstrap
```

3. Deploy (make sure docker engine is running)

```bash 
cdk deploy
```

4. Test with this JSON using API endpoint url:

```json
{
  "messageUUID": "05ceddd6-67e2-429a-a9c3-ea3edf6dbc7e",
  "messageText": "This is a placeholder message.",
  "messageDatetime": "2025-06-01 12:30:00"
}
```

Invoke-RestMethod -Uri "https://APIENDPOINT/messages" `
>>   -Method POST `
>>   -Headers @{ "Content-Type" = "application/json" } `
>>   -Body '{"messageUUID": "05ceddd6-67e2-429a-a9c3-ea3edf6dbc7e", "messageText": "This is a test message", "messageDatetime": "2025-06-09 23:45:00"}'

5. Run unit tests

```bash
pip install pytest boto3
python -m pytest    
```

6. Clean up

```bash
cdk destroy 
```
