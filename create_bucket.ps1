Write-Host "Waiting for LocalStack..."
Start-Sleep -Seconds 3

$awsCmd = "aws"
$commonArgs = @(
    "--endpoint-url", "http://localhost:4566",
    "--region", "us-east-1"
)

$bucket = "memory-vault"

Write-Host "Checking if bucket '$bucket' exists..."

$headArgs = $commonArgs + @("s3api", "head-bucket", "--bucket", $bucket)
& $awsCmd $headArgs 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "Bucket already exists: $bucket"
}
else {
    Write-Host "Creating bucket: $bucket"
    $createArgs = $commonArgs + @("s3api", "create-bucket", "--bucket", $bucket)
    & $awsCmd $createArgs
}

Write-Host "Bucket ready."
