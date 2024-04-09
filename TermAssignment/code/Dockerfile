FROM python:3.9

WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Set environment variables
ENV AWS_ACCESS_KEY_ID="ASIASXFL5EGFBMA3RHX5"
ENV AWS_SECRET_ACCESS_KEY="QzRU0/18NYdV7uusLhsrvzhXNGlFLUQc5h8MFnBO"
ENV AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjENj//////////wEaCXVzLXdlc3QtMiJGMEQCIB7ujWz7/xO3X2QqbWeHV33mGLyJZcuVI6g96QX1HQV0AiBVSqb2orunCygMwHUXZfmZRW0WUbGDppP7coc+PQOqWSqxAggQEAEaDDE4NzE5MTU5OTQ5OCIMHz8dcukImvvierKfKo4CysA/+mE+w5wFY0AiO6ugPtXZ8/KQUS45mSGWD++2uE6lKgL8K0DqECS95ABmvGgEuBVu7j36Wc9u4qL27jo+jICoHxyrQGQsV8mbMyMEfTNphBQe1vkJXoVVCTAVY/05LHiLS7KLXexG9FFdk/5zWDCw/X/0ZF9lEL+aAVuqZbPLQn5IKdldGO0oMcZZQ/DDplAGhDcSz01PYwa02aCgDF8tSN70sCHHixrIPioLtEoTUPNBD0iOR/+JqdcYH7FcxEzIcpGYY2VBB4NY1NTbofjg/ckmq3mldbJx7AYHi2SqH7DjvgOn3Zu0znnM1n/bPhiL4sJ7D72j4njL6+f/h8Mnu3BCsqYYGcfX/O71MKfY07AGOp4BAxWomOBdAnrjkrG5R5z9biwuLX4uzAR0pvRJU9oxpr80EwT3pxoPzXE/scTMk1JHxG3hBdI+3ngi2gv+jxaj78vzB8Csid7hULiTEXMlmxLPMR8qNHwEAR6M6AwdervkQgTenu2Tzb2bvN7vGdZjsRGv1wdH+1szjK1d1eZxUCzq1ZLAmb3+G+CILkkrgpXive1UBnXhz6IVfq4NUwM="
ENV S3_BUCKET_NAME="shrav6-visualization-bucket"
ENV S3_CSV_FILE_NAME="dataset.csv"
ENV LAMBDA_FUNCTION_NAME="send-sns-lambda"
ENV SNS_TOPIC_NAME="SalesSNSReport"

# Copy the rest of the application code
COPY . .

CMD ["python", "app.py"]
