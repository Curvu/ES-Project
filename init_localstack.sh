#!/bin/bash

set -e

AWS_DIR="/home/curvu/uni/ES/ES-Project/backend/api/AWS"

echo "Creating Dynamodb table..."
export PYTHONPATH="$HOME/.local/lib/python3.10/site-packages:$PYTHONPATH"
python3 "$AWS_DIR/init_dynamodb.py"

echo "Deploying Lambda function..."
cd "$AWS_DIR/lambdas"

for file in *.py; do
  function_name=$(basename "$file" .py)
  echo "📦 Packaging and deploying $function_name"

  zip -q function.zip "$file"

  # Delete if already exists
  aws --endpoint-url=http://localhost:4566 lambda delete-function \
      --function-name "$function_name" 2>/dev/null || true

  aws --endpoint-url=http://localhost:4566 lambda create-function \
    --function-name "$function_name" \
    --runtime python3.8 \
    --role arn:aws:iam::000000000000:role/service-role-for-lambda \
    --handler "${function_name}.lambda_handler" \
    --zip-file fileb://function.zip

  rm function.zip
done


echo "Deploying Step Function..."
cd "$AWS_DIR/stepfunctions"

# Delete if already exists
aws --endpoint-url=http://localhost:4566 stepfunctions delete-state-machine \
    --state-machine-arn arn:aws:states:us-east-1:000000000000:stateMachine:BookingWorkflow 2>/dev/null || true

aws --endpoint-url=http://localhost:4566 stepfunctions create-state-machine \
    --name "BookingWorkflow" \
    --definition file://booking.json \
    --role-arn arn:aws:iam::000000000000:role/StepFunctionsExecutionRole

echo "✅ Deployment complete!"