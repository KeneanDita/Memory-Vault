Write-Host "Creating DynamoDB tables for Memory Vault..."

$endpoint = "http://localhost:4566"
$region = "us-east-1"

# ---- Notes Table ----
aws dynamodb create-table `
  --table-name MemoryVaultNotes `
  --attribute-definitions AttributeName=note_id,AttributeType=S `
  --key-schema AttributeName=note_id,KeyType=HASH `
  --billing-mode PAY_PER_REQUEST `
  --endpoint-url $endpoint `
  --region $region

# ---- Images Table ----
aws dynamodb create-table `
  --table-name MemoryVaultImages `
  --attribute-definitions AttributeName=image_id,AttributeType=S `
  --key-schema AttributeName=image_id,KeyType=HASH `
  --billing-mode PAY_PER_REQUEST `
  --endpoint-url $endpoint `
  --region $region

# ---- Videos Table ----
aws dynamodb create-table `
  --table-name MemoryVaultVideos `
  --attribute-definitions AttributeName=video_id,AttributeType=S `
  --key-schema AttributeName=video_id,KeyType=HASH `
  --billing-mode PAY_PER_REQUEST `
  --endpoint-url $endpoint `
  --region $region

Write-Host "`nAll tables created successfully."
