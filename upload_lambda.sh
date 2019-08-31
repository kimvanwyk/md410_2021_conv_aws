zip -j lambda.zip app/reg_form_data_create.py
aws lambda update-function-code --function-name reg_form_data_create --zip-file fileb://lambda.zip
