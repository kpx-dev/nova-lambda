FROM public.ecr.aws/lambda/python:3.12

# Copy requirements and install dependencies
COPY app/requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy application code
COPY app/ ${LAMBDA_TASK_ROOT}

# Set the CMD to the Lambda handler
CMD ["lambda_handler.handler"]
