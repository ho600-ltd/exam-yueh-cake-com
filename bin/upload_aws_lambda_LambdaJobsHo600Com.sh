DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${DIR}/../aws_lambda/
rm -rf LambdaJobsHo600Com_function.zip
zip LambdaJobsHo600Com_function.zip LambdaJobsHo600Com.py
mv LambdaJobsHo600Com_function.zip ${DIR}
cd ${DIR}
aws --profile default --region us-west-2 lambda update-function-code --function-name LambdaJobsHo600Com --zip-file fileb://${DIR}/LambdaJobsHo600Com_function.zip