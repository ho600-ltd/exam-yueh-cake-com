PYTHON3_VERSION_NUMBER=`python3 -c "print('{}.{}'.format(*(__import__('sys').version_info[:2])))"`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="${DIR}/../aws_lambda/upload_pgp_file_to_s3"
cd $BASE_DIR
find . -name "*.pyc" -exec rm -rf {} \;
${DIR}/../.py3env/bin/pip3 install pgpdump==1.5
rm -rf upload_pgp_file_to_s3.zip
cd ${DIR}/../.py3env/lib/python${PYTHON3_VERSION_NUMBER}/site-packages
zip -r9 ${BASE_DIR}/upload_pgp_file_to_s3.zip pgpdump*
cd $BASE_DIR
zip -g upload_pgp_file_to_s3.zip lambda_function.py
mv upload_pgp_file_to_s3.zip $DIR
cd ${DIR}
aws --profile default --region us-west-2 lambda update-function-code --function-name uploadpgpfiletos3 --zip-file fileb://${DIR}/upload_pgp_file_to_s3.zip
