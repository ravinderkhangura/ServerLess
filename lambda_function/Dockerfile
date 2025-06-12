FROM public.ecr.aws/lambda/python:3.11

COPY handler.py ./

RUN pip install boto3

CMD ["handler.lambda_handler"]
