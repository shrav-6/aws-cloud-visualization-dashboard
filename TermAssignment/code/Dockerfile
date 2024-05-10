FROM python:3.9

WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Set environment variables
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_SESSION_TOKEN=""
ENV S3_BUCKET_NAME="shrav6-visualization-bucket"
ENV S3_CSV_FILE_NAME="dataset.csv"
ENV LAMBDA_FUNCTION_NAME="send-sns-lambda"
ENV SNS_TOPIC_NAME="SalesSNSReport"

# Copy the rest of the application code
COPY . .

CMD ["python", "app.py"]
