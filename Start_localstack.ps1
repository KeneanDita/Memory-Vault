# Stop any existing LocalStack container
docker stop localstack 2>$null
docker rm localstack 2>$null

# Start LocalStack with test environment variables
docker run -d `
  --name localstack `
  -p 4566:4566 `
  -e SERVICES="s3,sqs,sns,dynamodb,lambda,iam" `
  -e DEFAULT_REGION="us-east-1" `
  -e AWS_ACCESS_KEY_ID="test" `
  -e AWS_SECRET_ACCESS_KEY="test" `
  -e AWS_DEFAULT_REGION="us-east-1" `
  -e DEBUG=1 `
  -e DATA_DIR="/tmp/localstack/data" `
  -v "//var/run/docker.sock:/var/run/docker.sock" `
  localstack/localstack

Write-Host "LocalStack started on http://localhost:4566"
