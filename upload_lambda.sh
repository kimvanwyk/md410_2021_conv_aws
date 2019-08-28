zip -j lambda.zip app/lambda_function.py
aws lambda update-function-code --function-name reg_form_submit --zip-file fileb://lambda.zip
