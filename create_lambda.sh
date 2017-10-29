
aws s3 cp  lambda_build.zip s3://2tears

aws lambda   delete-function --function-name newscraper


aws lambda create-function \
--region us-west-2 \
--function-name newscraper \
--code S3Bucket=2tears,S3Key=lambda_build.zip \
--role arn:aws:iam::208673317854:role/service-role/MindMachine  \
--handler lambda_function.lambda_handler \
--runtime python3.6 \
--profile default \
--timeout 15 \
--memory-size 1024








